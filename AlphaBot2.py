from AlphaBot import AlphaBot
from PCA9685 import PCA9685
import time
import math

class AlphaBot2(AlphaBot):

	def __init__(self):
		super().__init__()
		self.pwm = PCA9685(0x40, True)
		self.pwm.setPWMFreq(50)

	def lookAt(self, theta, phi):
		super().lookAt(theta, phi)
		hpulse = ((theta+180)/360)*2000+500
		vpulse = ((-phi+180)/360)*2000+500
		self.pwm.setServoPulse(0,hpulse)
		time.sleep(0.02)
		self.pwm.setServoPulse(1,vpulse)
		time.sleep(0.02)
