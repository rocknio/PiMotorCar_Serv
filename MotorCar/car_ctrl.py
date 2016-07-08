# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from MotorCar.wheel import Wheel

author = "Ryan Song"


class Car(object):
    def __init__(self, front_left_wheel, front_right_wheel, rear_left_wheel, rear_right_wheel):
        self.wheels = {
            "fl": front_left_wheel,
            "fr": front_right_wheel,
            "rl": rear_left_wheel,
            "rr": rear_right_wheel
        }

        GPIO.setmode(GPIO.BOARD)
        for wheel in self.wheels:
            if isinstance(wheel, Wheel):
                GPIO.setup(wheel.pin1, GPIO.OUT)
                GPIO.setup(wheel.pin2, GPIO.OUT)

    def __del__(self):
        self.car_stop()
        GPIO.cleanup()

    def car_forward(self):
        GPIO.output(self.wheels["fl"].pin1, 1)
        GPIO.output(self.wheels["fl"].pin2, 0)
        GPIO.output(self.wheels["fr"].pin1, 1)
        GPIO.output(self.wheels["fr"].pin2, 0)

        GPIO.output(self.wheels["rl"].pin1, 1)
        GPIO.output(self.wheels["rl"].pin2, 0)
        GPIO.output(self.wheels["rr"].pin1, 1)
        GPIO.output(self.wheels["rr"].pin2, 0)

    def car_astern(self):
        GPIO.output(self.wheels["fl"].pin1, 0)
        GPIO.output(self.wheels["fl"].pin2, 1)
        GPIO.output(self.wheels["fr"].pin1, 0)
        GPIO.output(self.wheels["fr"].pin2, 1)

        GPIO.output(self.wheels["rl"].pin1, 0)
        GPIO.output(self.wheels["rl"].pin2, 1)
        GPIO.output(self.wheels["rr"].pin1, 0)
        GPIO.output(self.wheels["rr"].pin2, 1)

    def car_turn_left(self):
        GPIO.output(self.wheels["fl"].pin1, 0)
        GPIO.output(self.wheels["fl"].pin2, 1)
        GPIO.output(self.wheels["fr"].pin1, 0)
        GPIO.output(self.wheels["fr"].pin2, 0)

        GPIO.output(self.wheels["rl"].pin1, 0)
        GPIO.output(self.wheels["rl"].pin2, 1)
        GPIO.output(self.wheels["rr"].pin1, 0)
        GPIO.output(self.wheels["rr"].pin2, 0)

    def car_turn_right(self):
        GPIO.output(self.wheels["fl"].pin1, 0)
        GPIO.output(self.wheels["fl"].pin2, 0)
        GPIO.output(self.wheels["fr"].pin1, 1)
        GPIO.output(self.wheels["fr"].pin2, 0)

        GPIO.output(self.wheels["rl"].pin1, 0)
        GPIO.output(self.wheels["rl"].pin2, 0)
        GPIO.output(self.wheels["rr"].pin1, 1)
        GPIO.output(self.wheels["rr"].pin2, 0)

    def car_stop(self):
        GPIO.output(self.wheels["fl"].pin1, 0)
        GPIO.output(self.wheels["fl"].pin2, 0)
        GPIO.output(self.wheels["fr"].pin1, 0)
        GPIO.output(self.wheels["fr"].pin2, 0)

        GPIO.output(self.wheels["rl"].pin1, 0)
        GPIO.output(self.wheels["rl"].pin2, 0)
        GPIO.output(self.wheels["rr"].pin1, 0)
        GPIO.output(self.wheels["rr"].pin2, 0)
