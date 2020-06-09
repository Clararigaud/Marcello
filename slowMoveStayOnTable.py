#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import AlphaBot_clara
CS = 5
Clock = 25
Address = 24
DataOut = 23
Button = 7

class TRSensor(object):
	def __init__(self,numSensors = 5):
		self.numSensors = numSensors
		self.calibratedMin = [0] * self.numSensors
		self.calibratedMax = [1023] * self.numSensors
		self.last_value = 0
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(Clock,GPIO.OUT)
		GPIO.setup(Address,GPIO.OUT)
		GPIO.setup(CS,GPIO.OUT)
		GPIO.setup(DataOut,GPIO.IN,GPIO.PUD_UP)
		GPIO.setup(Button,GPIO.IN,GPIO.PUD_UP)
		
	def AnalogRead(self):
		value = [0]*(self.numSensors+1)
		#Read Channel0~channel6 AD value
		for j in range(0,self.numSensors+1):
			GPIO.output(CS, GPIO.LOW)
			for i in range(0,4):
				#sent 4-bit Address
				if(((j) >> (3 - i)) & 0x01):
					GPIO.output(Address,GPIO.HIGH)
				else:
					GPIO.output(Address,GPIO.LOW)
				#read MSB 4-bit data
				value[j] <<= 1
				if(GPIO.input(DataOut)):
					value[j] |= 0x01
				GPIO.output(Clock,GPIO.HIGH)
				GPIO.output(Clock,GPIO.LOW)
			for i in range(0,6):
				#read LSB 8-bit data
				value[j] <<= 1
				if(GPIO.input(DataOut)):
					value[j] |= 0x01
				GPIO.output(Clock,GPIO.HIGH)
				GPIO.output(Clock,GPIO.LOW)
			time.sleep(0.0001)
			GPIO.output(CS,GPIO.HIGH)
		return value[1:]
		
	"""
	Reads the sensors 10 times and uses the results for
	calibration.  The sensor values are not returned; instead, the
	maximum and minimum values found over time are stored internally
	and used for the readCalibrated() method.
	"""
	def calibrate(self):
		max_sensor_values = [0]*self.numSensors
		min_sensor_values = [0]*self.numSensors
		for j in range(0,10):
		
			sensor_values = self.AnalogRead();
			
			for i in range(0,self.numSensors):
			
				# set the max we found THIS time
				if((j == 0) or max_sensor_values[i] < sensor_values[i]):
					max_sensor_values[i] = sensor_values[i]

				# set the min we found THIS time
				if((j == 0) or min_sensor_values[i] > sensor_values[i]):
					min_sensor_values[i] = sensor_values[i]

		# record the min and max calibration values
		for i in range(0,self.numSensors):
			if(min_sensor_values[i] > self.calibratedMin[i]):
				self.calibratedMin[i] = min_sensor_values[i]
			if(max_sensor_values[i] < self.calibratedMax[i]):
				self.calibratedMax[i] = max_sensor_values[i]

	"""
	Returns values calibrated to a value between 0 and 1000, where
	0 corresponds to the minimum value read by calibrate() and 1000
	corresponds to the maximum value.  Calibration values are
	stored separately for each sensor, so that differences in the
	sensors are accounted for automatically.
	"""
	def	readCalibrated(self):
		value = 0
		#read the needed values
		sensor_values = self.AnalogRead();

		for i in range (0,self.numSensors):

			denominator = self.calibratedMax[i] - self.calibratedMin[i]

			if(denominator != 0):
				value = (sensor_values[i] - self.calibratedMin[i])* 1000 / denominator
				
			if(value < 0):
				value = 0
			elif(value > 1000):
				value = 1000
				
			sensor_values[i] = value
		
		#print("readCalibrated",sensor_values)
		return sensor_values
			
	"""
	Operates the same as read calibrated, but also returns an
	estimated position of the robot with respect to a line. The
	estimate is made using a weighted average of the sensor indices
	multiplied by 1000, so that a return value of 0 indicates that
	the line is directly below sensor 0, a return value of 1000
	indicates that the line is directly below sensor 1, 2000
	indicates that it's below sensor 2000, etc.  Intermediate
	values indicate that the line is between two sensors.  The
	formula is:

	   0*value0 + 1000*value1 + 2000*value2 + ...
	   --------------------------------------------
			 value0  +  value1  +  value2 + ...

	By default, this function assumes a dark line (high values)
	surrounded by white (low values).  If your line is light on
	black, set the optional second argument white_line to true.  In
	this case, each sensor value will be replaced by (1000-value)
	before the averaging.
	"""
	def readLine(self, white_line = 0):

		sensor_values = self.readCalibrated()
		avg = 0
		sum = 0
		on_line = 0
		for i in range(0,self.numSensors):
			value = sensor_values[i]
			if(white_line):
				value = 1000-value
			# keep track of whether we see the line at all
			if(value > 200):
				on_line = 1
				
			# only average in values that are above a noise threshold
			if(value > 50):
				avg += value * (i * 1000);  # this is for the weighted total,
				sum += value;                  #this is for the denominator 

		if(on_line != 1):
			# If it last read to the left of center, return 0.
			if(self.last_value < (self.numSensors - 1)*1000/2):
				#print("left")
				self.last_value = 0;
	
			# If it last read to the right of center, return the max.
			else:
				#print("right")
				self.last_value = (self.numSensors - 1)*1000
		else:
			self.last_value = avg/sum
		
		return self.last_value,sensor_values
	

def edgeDetected():
	tableEdge = False
	sensors = TR.AnalogRead()
	print(sensors)
	for s in sensors : 
		if s < 150 :
			tableEdge = True
			break
	return tableEdge

# Simple example prints accel/mag data once per second:
if __name__ == '__main__':
	TR = TRSensor()
	Bot = AlphaBot_clara.AlphaBot2()
	Bot.setPWMA(8)
	Bot.setPWMB(8)
	while True:
		tableEdge = False
		tableEdge  = edgeDetected()

		if tableEdge :
			print("AAAH DEMI TOUUUUR")
			Bot.setPWMA(50)
			Bot.setPWMB(50)
			while(edgeDetected()):
				Bot.backward()
			Bot.setPWMA(8)
			Bot.setPWMB(8)
			Bot.left()
			time.sleep(1)
		else :
			print("FUUFUFU LIFE'S NICE")
			Bot.forward()
		time.sleep(0.2)


			 
