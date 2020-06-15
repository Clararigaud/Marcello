# camera servo
from PCA9685 import PCA9685
import time

def sayYes(step = 5, numberTime = 2):
	VPulse = 1500
	pwm.setServoPulse(1,VPulse)
	initialPos = VPulse
	while(VPulse<2500):
		VPulse += step
		pwm.setServoPulse(1,VPulse)
		print(pwm.getServoPulse(1))
		time.sleep(0.02)    

	while(VPulse>500):
		VPulse -= step
		pwm.setServoPulse(1,VPulse)
		print(pwm.getServoPulse(1))
		time.sleep(0.02)    

	while(VPulse<initialPos):
		VPulse += step
		pwm.setServoPulse(1,VPulse)
		print(pwm.getServoPulse(1))
		time.sleep(0.02)    

def sayNo(step = 10, numberTime = 2):
	HPulse = 1500
	initialPos = HPulse
	while(HPulse<2500):
		HPulse += step
		pwm.setServoPulse(0,HPulse)

	while(HPulse>500):
		HPulse -= step
		pwm.setServoPulse(0,HPulse)

	while(HPulse<initialPos):
		HPulse += step
		pwm.setServoPulse(0,HPulse)

if __name__=='__main__':
	pwm = PCA9685(0x40)
	pwm.setPWMFreq(50)

	HPulse = 1500  #Sets the initial Pulse 500-2500
	VPulse = 1500  #Sets the initial Pulse 500-2500

	pwm.setServoPulse(1,VPulse)
	pwm.setServoPulse(0,HPulse)

	sayYes()
	sayYes()
	sayYes()
	#sayNo()