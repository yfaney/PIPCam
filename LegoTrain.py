import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class LED:
	def __init__(self, wh_pin, ir_pin):
		self.wh_pin = wh_pin
		self.ir_pin = ir_pin
		self.wh_led = False
		self.ir_led = False
		GPIO.setup(wh_pin, GPIO.OUT)
		GPIO.setup(ir_pin, GPIO.OUT)
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

class Motor:
	def __init__(self, fw_pin, bw_pin, wakeup_pin):
		self.pin_forward = fw_pin
		self.pin_backward = bw_pin
		self.pin_wakeup = wakeup_pin
		GPIO.setup(fw_pin, GPIO.OUT)
		GPIO.setup(bw_pin, GPIO.OUT)
		GPIO.setup(wakeup_pin, GPIO.OUT)
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

def cleanup():
	GPIO.cleanup()
