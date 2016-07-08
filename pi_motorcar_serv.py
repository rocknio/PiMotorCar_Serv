# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.websocket
import tornado.web
from tornado import ioloop
from MotorCar.car_ctrl import motor_car

author = "Ryan Song"

# 只允许一个连接
isAlreadyConnect = 0


class WsHandle(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self):
        """
        新客户端连接
        """
        print('client has connected! {}'.format(str(id(self))))

    def on_close(self):
        """
        连接断开
        """
        motor_car.car_stop()

        global isAlreadyConnect
        isAlreadyConnect = 0
        print("client has disconnected! {}".format(str(id(self))))

    def on_message(self, message):
        """
        处理客户端主动上行的消息
        :param message: 消息体内容
        """
        print("Recv = {}".format(message))
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
            print("unknown command = {}".format(message))

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
        print("start http server at: {}".format(9090))

        ioloop.IOLoop.instance().start()
    except Exception as e:
        print('Exception: %s'.format(e))

if __name__ == "__main__":
    start_serv()
