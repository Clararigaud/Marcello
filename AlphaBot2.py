from AlphaBot import AlphaBot
from PCA9685 import PCA9685
import RPi.GPIO as GPIO
from datetime import datetime
import time
import math

class AlphaBot2(AlphaBot):
	def __init__(self):
		self.pwm = PCA9685(0x40, True)
		self.pwm.setPWMFreq(50)
		super().__init__()

	def lookAt(self, theta, phi):
		super().lookAt(theta, phi)
		hpulse = ((theta+180)/360)*2000+500
		vpulse = ((-phi+180)/360)*2000+500
		self.pwm.setServoPulse(0,hpulse)
		time.sleep(0.02)
		self.pwm.setServoPulse(1,vpulse)
		time.sleep(0.02)

	def stop(self):
		super().stop()
		self.pwm.stop()
		print("Bot stopping")

	def capture_image(self,dest):
		now = datetime.now()
		filename = 'screenshot-%s.png'%(now.strftime("%m%d%Y%H%M%S"))
		path = 'temp/'+filename
		dest = "images/"
		super().capture_image(dest)