# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.websocket
import tornado.web
from tornado import ioloop
from MotorCar.car_ctrl import Car
from MotorCar.wheel import Wheel
import logging
import logging.handlers

author = "Ryan Song"

# 只允许一个连接
isAlreadyConnect = 0

# 车辆配置
fl_wheel = Wheel(13, 15)
fr_wheel = Wheel(22, 24)
rl_wheel = Wheel(6, 8)
rr_wheel = Wheel(12, 14)
motor_car = Car(fl_wheel, fr_wheel, rl_wheel, rr_wheel)


def init_logging():
    """
    日志文件设置，同时打印在日志文件和屏幕上
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    file_log = logging.handlers.TimedRotatingFileHandler('motorcar.log', 'MIDNIGHT', 1, 0)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)-7s] [%(module)s:%(filename)s-%(funcName)s-%(lineno)d] %(message)s')
    sh.setFormatter(formatter)
    file_log.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(file_log)

    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))


class WsHandle(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self):
        """
        新客户端连接
        """
        logging.info('client has connected! {}'.format(str(id(self))))

    def on_close(self):
        """
        连接断开
        """
        motor_car.car_stop()

        global isAlreadyConnect
        isAlreadyConnect = 0
        logging.info("client has disconnected! {}".format(str(id(self))))

    def on_message(self, message):
        """
        处理客户端主动上行的消息
        :param message: 消息体内容
        """
        logging.info("Recv = {}".format(message))
        if message == "forward":
            motor_car.car_forward()
        elif message == "astern":
            motor_car.car_astern()
        elif message == "turn_left":
            motor_car.car_turn_left()
        elif message == "turn_right":
            motor_car.car_turn_right()
        elif message == "stop_left":
            pass
        elif message == "stop_right":
            pass
        elif message == "stop_all":
            motor_car.car_stop()
        else:
            logging.error("unknown command = {}".format(message))

    def check_origin(self, origin):
        """
        websocket请求有效性检查
        :param origin:
        :return:
        """
        global isAlreadyConnect
        if isAlreadyConnect == 0:
            isAlreadyConnect = 1
            return True
        else:
            return False


def start_serv():
    try:
        init_logging()

        # http server url配置
        app_handlers = [
            # websocket接口
            (r'/ws', WsHandle),
        ]

        app = tornado.web.Application(
            handlers=app_handlers
        )

        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(9090)
        logging.info("start http server at: {}".format(9090))

        ioloop.IOLoop.instance().start()
    except Exception as e:
        logging.error('Exception: %s'.format(e))

if __name__ == "__main__":
    start_serv()
