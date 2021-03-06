#!/usr/bin/python3
#
# simple_tx_test.py
# 
# This python3 sent CAN messages out, with byte 7 increamenting each time.
# For use with PiCAN boards on the Raspberry Pi
# http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-2-p-1475.html
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 01-02-16 SK Pang
#
#
#


import RPi.GPIO as GPIO
import can
import time
import os


led = 22 #led on pican2 -> while data sending on.
GPIO.setmode(GPIO.BCM)    #choose BCM or BOARD  
GPIO.setwarnings(False)   
GPIO.setup(led,GPIO.OUT)  # set a port/pin as an output 
GPIO.output(led,True)     #set port/pin value to 1/GPIO.HIGH/True 

count = 0

print('\n\rCAN Rx test')
print('Bring up CAN0....')

# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 250000") #just writing os terminal
time.sleep(0.1)	
print('Press CTL-C to exit')

try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native') #in pican2 we use socket native
except OSError:
	print('Cannot find PiCAN board.')
	GPIO.output(led,False)
	exit()

# Main loop
try:
	while True:
		GPIO.output(led,True)	
		msg = can.Message(arbitration_id=0x7de,data=[0x01,0x01,0x01, 0x01, 0x01, 0x01,0x01, count & 0xff],extended_id=False) #1111 & count 
		bus.send(msg)
		count +=1
		time.sleep(2)
		GPIO.output(led,False)
		time.sleep(0.5)	
		print(count)	
		 

	
except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False)
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')