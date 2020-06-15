#!/usr/bin/python

import time
import math
import smbus

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:

  # Registers/etc.
  __SUBADR1            = 0x02
  __SUBADR2            = 0x03
  __SUBADR3            = 0x04
  __MODE1              = 0x00
  __PRESCALE           = 0xFE
  __LED0_ON_L          = 0x06
  __LED0_ON_H          = 0x07
  __LED0_OFF_L         = 0x08
  __LED0_OFF_H         = 0x09
  __ALLLED_ON_L        = 0xFA
  __ALLLED_ON_H        = 0xFB
  __ALLLED_OFF_L       = 0xFC
  __ALLLED_OFF_H       = 0xFD

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
    pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us
    self.setPWM(channel, 0, int(pulse))
  
  def lookAt(self, theta, phi):
    msb_phi = int(math.sin(math.pi*phi/180)<0)
    msb_theta = int(math.sin(math.pi*theta/180)<0)

    hori_angle = int(255 - msb_phi*(phi*255/90))
    vert_angle = int(255 - msb_theta*(theta*255/90))

    print("msb_phi: ",msb_phi)
    print("hori_angle: ",hori_angle)
    print("msb_theta: ",msb_theta)
    print("vert_angle: ",vert_angle)
    #horizontale phi
    self.write(self.__LED0_ON_L, 0 & 0xFF)
    self.write(self.__LED0_ON_H, 0 >> 8)
    self.write(self.__LED0_OFF_L, hori_angle & 0xFF) # 0-255
    self.write(self.__LED0_OFF_H, msb_phi >> 8) # 0,1

    #Vertical  theta
    self.write(self.__LED0_ON_L+4, 0 & 0xFF)
    self.write(self.__LED0_ON_H+4, 0 >> 8)
    self.write(self.__LED0_OFF_L+4, vert_angle & 0xFF) # 0-255
    self.write(self.__LED0_OFF_H+4, msb_theta >> 8)# 0,1,2

  def getPWM(self, channel):
    "Gets a single PWM channel"
    print("LED0_OFF_L", self.read(self.__LED0_OFF_L+4*channel))
    print("LED0_OFF_H", self.read(self.__LED0_OFF_H+4*channel))
    return self.read(self.__LED0_OFF_L+4*channel)

  def getServoPulse(self, channel):
    pulse = float(self.getPWM(channel))/4096*20000 
    return pulse

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
