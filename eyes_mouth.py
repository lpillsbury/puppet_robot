#!/usr/bin/python3
# in this code I have the different color eyes blink.
# you can stop or start it by pressing the button, but
# if you press the button at any time, the LEDs might go
# through their cycle before shutting off

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
g_eye = 18
b_eye =15
servoPIN =17
GPIO.setup(g_eye,GPIO.OUT)
GPIO.setup(b_eye,GPIO.OUT)
GPIO.setup(servoPIN, GPIO.OUT)
#GPIO.setup(23, GPIO.IN) # this was for the button


# I dont understand this
# it is from https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/
p = GPIO.PWM(servoPIN, 50)
p.start(2.5) # initialization

try:
    while True:
        p.ChangeDutyCycle(3)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        GPIO.output(g_eye,True)
        p.ChangeDutyCycle(6)
        time.sleep(1)
        GPIO.output(b_eye, True)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        GPIO.output(g_eye,False)
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        GPIO.output(b_eye,False)
        p.ChangeDutyCycle(2.5)
    
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    GPIO.output(b_eye,False)
    GPIO.output(g_eye,False)

