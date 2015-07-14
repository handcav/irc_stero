#!/usr/bin/python

import pylirc, time
import RPi.GPIO as GPIO

PN = [11, 7]
OK = 13
VL = [19, 15]
POWER = 21
STERO = 23

state = False
blocking = 0;
clk = 0.5

def sterocontrol():
	if state == True:
		GPIO.setup(PN[0], GPIO.OUT)
		GPIO.setup(PN[1], GPIO.OUT)
		GPIO.setup(VL[0], GPIO.OUT)
		GPIO.setup(VL[1], GPIO.OUT)
		GPIO.setup(POWER, GPIO.OUT)
		GPIO.setup(OK, GPIO.OUT)
		GPIO.output(STERO, 0)

	if state == False:
		GPIO.setup(PN[0], GPIO.IN)
		GPIO.setup(PN[1], GPIO.IN)
		GPIO.setup(VL[0], GPIO.IN)
		GPIO.setup(VL[1], GPIO.IN)
		GPIO.setup(POWER, GPIO.IN)
		GPIO.setup(OK, GPIO.IN)
		GPIO.output(STERO, 1)

def setup():
	global state
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(STERO, GPIO.OUT)
	pylirc.init("pylirc", "./conf", blocking)

def rencoder(re, wise):	#wise:0=anticlockwise, 1=clockwise
	if wise == 1:
		GPIO.output(re[1], 1)
		time.sleep(clk)
		GPIO.output(re[0], 1)
		time.sleep(clk)
		GPIO.output(re[1], 0)
		time.sleep(clk)
		GPIO.output(re[0], 0)
		time.sleep(clk)
	if wise == 0:
		GPIO.output(re[0], 1)
		time.sleep(clk)
		GPIO.output(re[1], 1)
		time.sleep(clk)
		GPIO.output(re[0], 0)
		time.sleep(clk)
		GPIO.output(re[1], 0)
		time.sleep(clk)

def IRC(config):
	global state
	if config == 'KEY_A':
		state = not state
		sterocontrol()
		print 'state = ', state
	if state == True:
		if config == 'KEY_VOLUMEUP':
			rencoder(VL, 1)
			print 'Volume up'
	
		if config == 'KEY_VOLUMEDOWN':
			rencoder(VL, 0)
			print 'Volume down'
	
		if config == 'KEY_PREVIOUS':
			rencoder(PN, 0)
			print 'Prevoius'
	
		if config == 'KEY_NEXT':
			rencoder(PN, 1)
			print 'Next'
	
		if config == 'KEY_PLAYPAUSE':
			GPIO.setup(POWER, 1)
			time.sleep(0.5)
			GPIO.setup(POWER, 0)
			time.sleep(0.5)
			print 'Power button pressed.'

def rc():
	s = pylirc.nextcode(1)
	
	while(s):
		for (code) in s:
#			print 'Command: ', code["config"] #For debug: Uncomment this
#			line to see the return value of buttons
			IRC(code["config"])
		if(not blocking):
			s = pylirc.nextcode(1)
		else:
			s = []

def loop():
	while True:
		rc()

def destroy():
	GPIO.cleanup()
	pylirc.exit()

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()

