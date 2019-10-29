#!/usr/bin/python3
# In this program, Blubbo the grouper fish plays
# With the user for 5 minutes. Blubbo introduces himself,
# then offers to sing. When Blubbo sings, he may also fart

import subprocess
import RPi.GPIO as GPIO
import time
import threading # read https://realpython.com/intro-to-python-threading/
import logging # info about how to use logging at https://realpython.com/python-logging/
import sys
import random # for random number generation at a few places

logging.basicConfig(level=logging.DEBUG)
logging.debug('Starting the program')
logging.debug('python version ' + sys.version)

# setup GPIO settings and pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
g_eye = 22
b_eye =27
r_eye = 17
servoPIN = 18
#g_eye2
#b_eye2
#r_eye2
# define the capacitive sensor pins here or in function?
# is function in this code or separate?

GPIO.setup(g_eye,GPIO.OUT)
GPIO.setup(b_eye,GPIO.OUT)
GPIO.setup(r_eye,GPIO.OUT)
#GPIO.setup(servoPIN, GPIO.OUT)

logging.debug('starting saying greeting')
# text = "My name is Blubbo. I am a fish. I like to sing. When you touch my fin, I will sing for you"
text = 'Hi I am Blubbo'
subprocess.call('espeak -s 125 -v en "%s" --stdout | aplay'%text, shell=True)
logging.debug('finished saying greeting')

blink_type=random.randint(1,3)
logging.debug(blink_type)
if blink_type == 1:
    GPIO.output(g_eye,True)
    time.sleep(3)
elif blink_type ==2:
    for i in range(0,5):
        GPIO.output(r_eye,True)
        time.sleep(0.5)
        GPIO.output(r_eye, False)
        time.sleep(0.3)
elif blink_type == 3:
    for i in range(0,5):
        GPIO.output(b_eye,150)
        time.sleep(0.5)
        GPIO.output(b_eye, 0)
        GPIO.output(r_eye, 100)
        time.sleep(0.3)
        
    
