#!/usr/bin/python

import time
import math
import smbus

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:

  # Registers/etc.
  __MODE1              = 0x00 # Mode register 1
  __PRESCALE           = 0xFE # prescaler for PWM output frequency
  __LED0_ON_L          = 0x06 # LED0 output and brightness control byte 0
  __LED0_ON_H          = 0x07 # LED0 output and brightness control byte 1
  __LED0_OFF_L         = 0x08 # LED0 output and brightness control byte 2
  __LED0_OFF_H         = 0x09 # LED0 output and brightness control byte 3

  __LED1_ON_L          = 0x0A # LED1 output and brightness control byte 0
  __LED1_ON_H          = 0x0B # LED1 output and brightness control byte 1
  __LED1_OFF_L         = 0x0C # LED1 output and brightness control byte 2
  __LED1_OFF_H         = 0x0D # LED1 output and brightness control byte 3

  def __init__(self, address=0x40, debug=False):
    self.bus = smbus.SMBus(1)
    self.address = address
    self.debug = debug
    if (self.debug):
      print("Reseting PCA9685")
    self.write(self.__MODE1, 0x00)
	
  def write(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    self.bus.write_byte_data(self.address, reg, value)
    if (self.debug):
      print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))
	  
  def read(self, reg):
    "Read an unsigned byte from the I2C device"
    result = self.bus.read_byte_data(self.address, reg)
    if (self.debug):
      print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
    return result
	
  def setPWMFreq(self, freq):
    "Sets the PWM frequency"
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    if (self.debug):
      print("Setting PWM frequency to %d Hz" % freq)
      print("Estimated pre-scale: %d" % prescaleval)
    prescale = math.floor(prescaleval + 0.5)
    if (self.debug):
      print("Final pre-scale: %d" % prescale)

    oldmode = self.read(self.__MODE1);
    newmode = (oldmode & 0x7F) | 0x10        # sleep
    self.write(self.__MODE1, newmode)        # go to sleep
    self.write(self.__PRESCALE, int(math.floor(prescale)))
    self.write(self.__MODE1, oldmode)
    time.sleep(0.005)
    self.write(self.__MODE1, oldmode | 0x80)

  def setPWM(self, channel, on, off):
    "Sets a single PWM channel"
    self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
    self.write(self.__LED0_ON_H+4*channel, on >> 8)
    self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
    self.write(self.__LED0_OFF_H+4*channel, off >> 8)
    if (self.debug):
      print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))
	  
  def setServoPulse(self, channel, pulse):
    "Sets the Servo Pulse,The PWM frequency must be 50HZ"
    pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us nb bits / period 1/f = 0,2 ms
    #print(pulse)
    self.setPWM(channel, 0, int(pulse))
  
  def lookAt(self, theta, phi):
    hpulse = ((theta+180)/360)*2000+500
    vpulse = ((-phi+180)/360)*2000+500


    self.setServoPulse(0,hpulse)
    time.sleep(0.02)
    self.setServoPulse(1,vpulse)
    time.sleep(0.02)

    
    # self.setServoPulse(0,0)
    # self.setServoPulse(1,0)

  def getPWM(self, channel):
    "Gets a single PWM channel"
    print("LED0_OFF_L", self.read(self.__LED0_OFF_L+4*channel))
    print("LED0_OFF_H", self.read(self.__LED0_OFF_H+4*channel))
    return self.read(self.__LED0_OFF_L+4*channel)

  def getServoPulse(self, channel):
    pulse = float(self.getPWM(channel))/4096*20000 
    return pulse

  def stop(self):
      self.write(self.__MODE1, 0x00)
      self.write(self.__PRESCALE, 0x00)
      self.setPWM(0, 0, 0)
      self.setPWM(1, 0, 0)

if __name__=='__main__':
 
  pwm = PCA9685(0x40, debug=True)
  pwm.setPWMFreq(50)
  while True:
   # setServoPulse(2,2500)
    for i in range(500,2500,10):  
      pwm.setServoPulse(0,i)   
      time.sleep(0.02)     
    
    for i in range(2500,500,-10):
      pwm.setServoPulse(0,i) 
      time.sleep(0.02)  
