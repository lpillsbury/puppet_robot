#!/usr/bin/python3
# In this program, Blubbo the grouper fish plays
# With the user for 5 minutes. Blubbo introduces himself,
# then offers to sing. When Blubbo sings, he may also fart
# Blubbo farts at random time intervals
# After 5 mins Blubbo says goodbye and the program ends
# The program can also end earlier upon user request (by touching other fin?)

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
capRin = 24
capRout = 12
capLin = 23

GPIO.setup(g_eye,GPIO.OUT)
GPIO.setup(b_eye,GPIO.OUT)
GPIO.setup(r_eye,GPIO.OUT)
# setup the cap sensors in cap read function
GPIO.setup(servoPIN, GPIO.OUT)

# make blub object from Blubbo class
blub = Blubbo()

# make one speak function for all of the talking
def say_greeting():
    logging.debug('starting speaking')
    subprocess.call('espeak -s 100 -v en "%s" --stdout | aplay'%blub.talk[0], shell=True)
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
    
def sing_song():
    whichsong = blub.song[2]
    logging.debug('which song')
    logging.debug(whichsong)
    pygame.mixer.init()
    pygame.mixer.music.load(blub.song[2])
    pygame.mixer.music.play()
    logging.debug('played birthday song')
    
def read_fin(): # should there be arguments about which fin wea re reading?
    for x in range (0,1900):
        level = cap_read(capRin, capRout)
        print('level')
        print(level)
        if level > 20:
            return True
        time.sleep(0.1)
        
def cap_read(inPin,outPin):
    total = 0
    timeout = 5000
    # set Send Pin Register low
    GPIO.setup(outPin, GPIO.OUT)
    GPIO.output(outPin, GPIO.LOW)
    
    # set receivePin Register low to make sure pullups are off 
    GPIO.setup(inPin, GPIO.OUT)
    GPIO.output(inPin, GPIO.LOW)
    GPIO.setup(inPin, GPIO.IN)
    
    # set send Pin High
    GPIO.output(outPin, GPIO.HIGH)
    
    # while receive pin is LOW AND total is positive value
    while( GPIO.input(inPin) == GPIO.LOW and total < timeout ):
        total+=1
    print('total after low: ', total)
    
    if ( total > timeout ):
        return -2 # total variable over timeout
        
     # set receive pin HIGH briefly to charge up fully - because the while loop above will exit when pin is ~ 2.5V 
    GPIO.setup( inPin, GPIO.OUT )
    GPIO.output( inPin, GPIO.HIGH )
    GPIO.setup( inPin, GPIO.IN )
    
    # set send Pin LOW
    GPIO.output( outPin, GPIO.LOW ) 

    # while receive pin is HIGH  AND total is less than timeout
    while (GPIO.input(inPin)==GPIO.HIGH and total < timeout) :
        total+=1
    print('total after high: ', total)
    
    if ( total >= timeout ):
        return -2
    else:
        return total

    
# define threads
greet = threading.Thread(target = say_greeting)
blink = threading.Thread(target = blink_eyes)
fart = threading.Thread(target = make_fart)
#sing = threading.Thread(target = sing_song)

if __name__=="__main__":
    blub.eyes_on(r_eye, g_eye, b_eye)
    greet.start()
    time.sleep(2)
    
    fart.start()
    blink.start()
    time.sleep(10)
    fart.join()
    blink.join()
    greet.join()
    sing_song()
    #make_fart()
    #sing.start() 
