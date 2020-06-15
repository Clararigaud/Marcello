# camera servo
from PCA9685 import PCA9685
import time

def sayYes(step = 20, numberTime = 2):
	VPulse = 500
	pwm.setServoPulse(1,VPulse)
	time.sleep(0.2)
	initialPos = VPulse
	print("vpulse: ", VPulse)
	print("doan\n\n")
	while(VPulse<2500):
		VPulse += step
		print("vpulse: ", VPulse)
		pwm.setServoPulse(1,VPulse)
		print(pwm.getServoPulse(1))
		time.sleep(0.02)    
	input()
	print("up\n\n")
	while(VPulse>500):
		print("vpulse: ", VPulse)
		VPulse -= step
		pwm.setServoPulse(1,VPulse)
		print(pwm.getServoPulse(1))
		time.sleep(0.02)    
	input()
	print("down\n\n")
	while(VPulse<2500):
		print("vpulse: ", VPulse)
		VPulse += step
		pwm.setServoPulse(1,VPulse)
		print(pwm.getServoPulse(1))
		time.sleep(0.02)    

def sayNo(step = 30, numberTime = 2):
	HPulse = 1500
	initialPos = HPulse
	while(HPulse<2500):
		HPulse += step
		pwm.setServoPulse(0,HPulse)
		print(pwm.getServoPulse(0))
	while(HPulse>500):
		HPulse -= step
		pwm.setServoPulse(0,HPulse)
		print(pwm.getServoPulse(0))
	while(HPulse<initialPos):
		HPulse += step
		pwm.setServoPulse(0,HPulse)
		print(pwm.getServoPulse(0))
if __name__=='__main__':
	pwm = PCA9685(0x40, True)
	pwm.setPWMFreq(50)

	# pwm.lookAt(0,0)

	# time.sleep(2)

	# pwm.lookAt(-90,0)

	# time.sleep(2)

	# pwm.lookAt(90,0)

	# time.sleep(2)

	# pwm.lookAt(0,0)

	# time.sleep(2)

	# pwm.lookAt(0,-90)

	# time.sleep(2)

	# pwm.lookAt(0,90)

	# time.sleep(2)
	HPulse = 0  #Sets the initial Pulse 500-2500
	VPulse = 0  #Sets the initial Pulse 500-2500

	pwm.setServoPulse(1,VPulse)
	pwm.setServoPulse(0,HPulse)

	sayYes()
	# # sayYes()
	# # sayYes()
	# sayNo()