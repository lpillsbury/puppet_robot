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
from Blubbo_classdef import Blubbo

logging.basicConfig(level=logging.DEBUG)
logging.debug('Starting the program')
logging.debug('python version ' + sys.version)

# setup GPIO settings and pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# red, green, blue eye pins, servo pin, right/left capacitive sensors
r_eye = 17
g_eye = 27
b_eye = 22
servoPIN = 18
capR = 24
capL = 23

GPIO.setup(g_eye,GPIO.OUT)
GPIO.setup(b_eye,GPIO.OUT)
GPIO.setup(r_eye,GPIO.OUT)
GPIO.setup(capR, GPIO.OUT)
GPIO.setup(capL, GPIO.OUT)
GPIO.setup(servoPIN, GPIO.OUT)

# make blub object from Blubbo class
blub = Blubbo()

def say_greeting():
    logging.debug('starting saying greeting')
    text = "My name is Blubbo. I am a fish. I like to sing. If you touch my fin, I will sing for you"
    subprocess.call('espeak -s 100 -v en "%s" --stdout | aplay'%text, shell=True)
    logging.debug('finished saying greeting')

def make_fart():
    whichfart = random.randint(1,7)
    logging.debug('which fart')
    logging.debug(whichfart)
    pygame.mixer.init()
    pygame.mixer.music.load(blub.fart[whichfart])
    pygame.mixer.music.play()
    
def blink_eyes():
    blink_type=random.randint(1,4)
    keep_blinking = fart.isAlive()
    while(keep_blinking == True):
        logging.debug('blinking')
        blub.blink(blink_type, r_eye, g_eye, b_eye)
        keep_blinking = fart.isAlive()
    fart.join()
    logging.debug('done blinking')
    
# define threads
greet = threading.Thread(target = say_greeting)
blink = threading.Thread(target = blink_eyes)
fart = threading.Thread(target = make_fart)

def main():
    greet.start()
    fart.start()
    blink.start()


if __name__=="__main__":
    main()
