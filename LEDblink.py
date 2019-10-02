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
GPIO.setup(g_eye,GPIO.OUT)
GPIO.setup(b_eye,GPIO.OUT)
GPIO.setup(servoPIN, GPIO.OUT)

# GPIO.setup(23, GPIO.IN) this was for a button

while True:
    GPIO.output(g_eye,True)
    time.sleep(1.5)
    GPIO.output(b_eye,True)
    time.sleep(0.4)
    GPIO.output(g_eye,False)
    time.sleep(0.5)
    GPIO.output(b_eye,False)
