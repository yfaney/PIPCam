#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# Constants about GPIO pins
LTrain_PWM_Forward = 24
LTrain_PWM_Reward = 23
LTrain_PIN_LED_WH = 25
LTrain_PIN_LED_IR = 27
LTrain_PIN_Motor_On = 22
GPIO.setmode(GPIO.BCM)

GPIO.setup(LTrain_PWM_Forward, GPIO.OUT)
GPIO.setup(LTrain_PWM_Reward, GPIO.OUT)
GPIO.setup(LTrain_PIN_LED_WH, GPIO.OUT)
GPIO.setup(LTrain_PIN_LED_IR, GPIO.OUT)
GPIO.setup(LTrain_PIN_Motor_On, GPIO.OUT)

class LTrain_LED:
	def __init__(self, wh_pin, ir_pin):
		self.wh_pin = wh_pin
		self.ir_pin = ir_pin
		self.wh_led = False
		self.ir_led = False
	def white_led(self, onoff):
		if onoff is True:
			if self.ir_led is True:
				GPIO.output(self.ir_pin, False)
				self.ir_led = False
		GPIO.output(self.wh_pin, onoff)
		self.wh_led = onoff
	def ir_led(self, onoff):
		if onoff is True:
			if self.wh_led is True:
				GPIO.output(self.wh_pin, False)
				self.wh_led = False
		GPIO.output(self.ir_pin, onoff)
		self.ir_led = onoff		

class LTrain_Motor:
	def __init__(self, fw_pin, bw_pin, wakeup_pin):
		self.pin_forward = fw_pin
		self.pin_backward = bw_pin
		self.pin_wakeup = wakeup_pin
		self.motor_fw = GPIO.PWM(fw_pin, 50)
		self.motor_bw = GPIO.PWM(bw_pin, 50)
		self.motor_fw.start(0)
		self.motor_bw.start(0)
		self.level_fw = 0
		self.level_bw = 0
	def finish_motor(self):
		GPIO.output(self.pin_wakeup, False)
		self.motor_fw.stop()
		self.motor_bw.stop()
	def go(self, level):
		if level is not 0:
			GPIO.output(self.pin_wakeup, True)
		else:
			GPIO.output(self.pin_wakeup, False)
		if level > 0:
			if self.level_bw > 0:
				self.motor_bw.ChangeDutyCycle(0)
				self.level_bw = 0
			self.motor_fw.ChangeDutyCycle(level)
			self.level_fw = level
		else:
			if self.level_fw > 0:
				self.motor_fw.ChangeDutyCycle(0)
				self.level_fw = 0
			self.motor_bw.ChangeDutyCycle(level * -1)
			self.level_bw = level * -1
	def stop(self):
		if self.level_fw > 0:
			self.motor_fw.ChangeDutyCycle(0)
			self.level_fw = 0
		elif self.level_bw > 0:
			self.motor_bw.ChangeDutyCycle(0)
			self.level_bw = 0
		GPIO.output(self.pin_wakeup, False)

train_led = LTrain_LED(LTrain_PIN_LED_WH, LTrain_PIN_LED_IR)
train_motor = LTrain_Motor(LTrain_PWM_Forward, LTrain_PWM_Reward, LTrain_PIN_Motor_On)

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

GPIO.cleanup()
