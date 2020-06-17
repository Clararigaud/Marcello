# camera servo
from PCA9685 import PCA9685
import time
import math

pwm = PCA9685(0x40, True)
pwm.setPWMFreq(50)
def sayYes():
	i = 0
	r = 90
	c = [0,0]
	while True : 
		phi = c[1]+math.cos(i)*r
		pwm.lookAt(c[0], phi)
		i+=1
		time.sleep(0.02)

def sayNo():
	i = 0
	r = 90
	c = [0,0]
	while True : 
		theta = c[0]+math.cos(i)*r
		pwm.lookAt(theta, c[1])
		i+=1
		time.sleep(0.02)
if __name__=='__main__':



	#Center
	maxR = 2500
	minR = 500

	#H
	pwm.setServoPulse(0,(maxR-minR)/2)
	print(pwm.getServoPulse(0))
	#V
	pwm.setServoPulse(1,(maxR-minR)/2)
	print(pwm.getServoPulse(1))

	time.sleep(2)


	#LEFT
	#H
	pwm.setServoPulse(0,maxR)
	print(pwm.getServoPulse(0))
	#V
	pwm.setServoPulse(1,(maxR-minR)/2)
	print(pwm.getServoPulse(1))


	time.sleep(2)

	#H
	pwm.setServoPulse(0,minR)
	print(pwm.getServoPulse(0))
	#V
	pwm.setServoPulse(1,(maxR-minR)/2)
	print(pwm.getServoPulse(1))


	time.sleep(2)

	#H
	pwm.setServoPulse(0,(maxR-minR)/2)
	print(pwm.getServoPulse(0))
	#V
	pwm.setServoPulse(1,maxR)
	print(pwm.getServoPulse(1))


	time.sleep(2)

	#H
	pwm.setServoPulse(0,(maxR-minR)/2)
	print(pwm.getServoPulse(0))
	#V
	pwm.setServoPulse(1,minR)
	print(pwm.getServoPulse(1))

	# pwm.lookAt(3,3)


	# pwm.lookAt(-60,3)

	# time.sleep(2)

	# pwm.lookAt(60,3)

	# time.sleep(2)

	# pwm.lookAt(3,3)

	# time.sleep(2)

	# pwm.lookAt(3,-60)

	# time.sleep(2)

	# pwm.lookAt(3,60)

	# time.sleep(2)

	pwm.stop()
	# HPulse = 0  #Sets the initial Pulse 500-2500
	# VPulse = 0  #Sets the initial Pulse 500-2500

	# pwm.setServoPulse(1,VPulse)
	# pwm.setServoPulse(0,HPulse)

	# sayYes()
	# # sayYes()
	# # sayYes()
	# sayNo()