#!/usr/bin/python

import LegoTrain as Train
import time

# Constants about GPIO pins
PWM_Forward = 24
PWM_Reward = 23
PIN_LED_WH = 25
PIN_LED_IR = 27
PIN_Motor_On = 22

train_led = Train.LED(PIN_LED_WH, PIN_LED_IR)
train_motor = Train.Motor(PWM_Forward, PWM_Reward, PIN_Motor_On)

# test functions

train_led.white_led(True)
time.sleep(2)
train_led.white_led(False)
time.sleep(2)

train_motor.go(20)
time.sleep(2)
train_motor.go(0)
time.sleep(2)
train_motor.go(-20)
time.sleep(2)
train_motor.stop()

Train.cleanup()
