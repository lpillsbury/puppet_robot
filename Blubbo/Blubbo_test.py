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
import pygame

logging.basicConfig(level=logging.DEBUG)
logging.debug('Starting the program')
logging.debug('python version ' + sys.version)

# setup GPIO settings and pins
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
g_eye = 25
b_eye =23
r_eye = 17
servoPIN = 18

# define the capacitive sensor pins here or in function?
# is function in this code or separate?

GPIO.setup(g_eye,GPIO.OUT)
GPIO.setup(b_eye,GPIO.OUT)
GPIO.setup(r_eye,GPIO.OUT)
#GPIO.setup(servoPIN, GPIO.OUT)

logging.debug('starting saying greeting')
# text = "My name is Blubbo. I am a fish. I like to sing. When you touch my fin, I will sing for you"
text = 'Hi I am Blubbo'
subprocess.call('espeak -s 100 -v en-us "%s" --stdout | aplay'%text, shell=True)
logging.debug('finished saying greeting')
pygame.mixer.init()
pygame.mixer.music.load("fart1.mp3")
pygame.mixer.music.play()
time.sleep(5)
pygame.mixer.music.load("I Love Rock N Roll.mp3")
pygame.mixer.music.play()

blink_type=random.randint(1,3)
logging.debug(blink_type)

GPIO.output(r_eye, False)
GPIO.output(g_eye, False)
GPIO.output(b_eye, False)

