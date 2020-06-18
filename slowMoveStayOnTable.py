#!/usr/bin/python
# Free walk ( go forward, turn when edge of the table detected) Only using ir sensors located under the robot ( not very effective )
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2

def edgeDetected(bot):
	tableEdge = False
	sensors = bot.getTRSensorsValue()
	print(sensors)
	for s in sensors : 
		if s < 150 :
			tableEdge = True
			break
	return tableEdge

if __name__ == '__main__':
	Bot = AlphaBot2()
	Bot.setPWMA(8)  # Speed
	Bot.setPWMB(8)
	while True:
		tableEdge = False
		tableEdge  = edgeDetected(Bot)

		if tableEdge :
			print("AAAH DEMI TOUUUUR")
			Bot.setPWMA(50)
			Bot.setPWMB(50)
			while(edgeDetected()):
				Bot.backward()
			time.sleep(0.1)
			Bot.setPWMA(8)
			Bot.setPWMB(8)
			Bot.left()
			time.sleep(1)
		else :
			print("FUUFUFU LIFE'S NICE")
			Bot.forward()
		time.sleep(0.2)