#!/usr/bin/python3
# In this program, Blubbo the grouper fish plays
# With the user for 5 minutes. Blubbo introduces himself,
# then offers to sing. When Blubbo sings, he may also fart
# Blubbo farts at random time intervals
# After 5 mins Blubbo says goodbye and the program ends
# The program can also end earlier upon
# user request (by touching other fin?)

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

# global variables for thread states
# talk_state = 0; # when it is time to talk, talk_state will become 1
eye_state = 0; # this means all eyes are off, 1 for all eyes on and 2 for blinking
pygame.mixer.init()

# make one speak function for all of the talking
def say_stuff(talk_type):
    # Blubbo talks to introduce himself and to say goodbye.
    # in the class Blubbo talk[0] is for greeting, talk[1] for goodbye
    # in the future, can add more talk_types
    
    # need to a this point start moving the mouth
#     global mouth_event
    mouth_event.set()
    
    logging.debug('starting speaking')
    time.sleep(2)
    # talk
    subprocess.call('espeak -s 100 -v en "%s" --stdout | aplay'%blub.talk[talk_type], shell=True)
    
    # stop mouth moving
    mouth_event.clear()
    time.sleep(5)
    logging.debug('finished talking')

def make_fart():
    # Even though farting and singing are both playing audio files,
    # these need to be separate functions because farting can happen while singing
    # and because farting is coupled with blinking whereas
    # singing is coupled with mouth movement
    global eye_state
    whichfart = random.randint(0,6)
    logging.debug('which fart')
    logging.debug(whichfart)
    eye_state = 2
    pygame.mixer.music.load(blub.fart[whichfart])
    pygame.mixer.music.play()
    eye_state = 1
    
def sing_song(which_song):
    # This function plays any audio file and couples it with moving the mouth
#     global mouth_event
    
    logging.debug('which song')
    logging.debug(which_song)
    
    
    # start moving the mouth
    mouth_event.set()
    pygame.mixer.music.load(blub.song[which_song])
    pygame.mixer.music.play()
    time.sleep(10)
    pygame.mixer.music.stop()
    # stop moving the mouth
    mouth_event.clear()
    
    logging.debug('played song')
    


def mouth_control():
    # If Blubbo is supposed to be talking or singing, talk_state will be 1
    # Blubbo will move his mouth.
    # If talk_state is 0 then Blubbo just waits
    # in the future there could be different mouth movements for singing vs talking
    logging.debug('started mouth control')
    while getattr(mouth, "do_run", True):
        if mouth_event.isSet():
            blub.move_mouth(servoPIN)
            logging.debug('called mouth moving function from Blubbo class')
        time.sleep(1) # small delay so that program doesn't trip over itself
        #logging.debug('talk state is: ')
        #logging.debug(mouth_event)
    logging.debug('ended mouth control')
    
def eye_control():
    # This function controls whether Blubbo should be eyes off, eyes steady, or blinking
    logging.debug('started eye control')
    while (time.time() < end_time): # this is an infinite loop
        logging.debug('eye thread is alive')
        logging.debug('current eye state: ')
        logging.debug(eye_state)
        if eye_state == 0:
            blub.eyes_off(r_eye, g_eye, b_eye)
        elif eye_state == 1:
            blub.eyes_on(r_eye, g_eye, b_eye)
        elif eye_state == 2:
            blink = random.randint(1,4)
        time.sleep(0.5) # small delay so that program doesn't trip over itself
    
# define threads
# change the targets
# there is one thread for moving the mouth
# another thread for eye state
# another for cap sensor state?
# talking is dependent on end and start
# singing dependent on cap sensor
# cap sensor has a state variable
# farting is also dependent on time does it need its own thread?

# farting, talking, singing are dependent on what happens
mouth = threading.Thread(target = mouth_control)
eyes = threading.Thread(target = eye_control)
mouth_event = threading.Event()


if __name__=="__main__":
    start_time = time.time()
    end_time = start_time + 60 # set the end time as 1 minute after start
    logging.debug('start time')
    logging.debug(start_time)
    mouth.start()
    #eyes.start()
    eye_state = 1
    say_stuff(0)
    #time.sleep(2)
    # set a random time when Blubbo will fart next
    next_fart = random.uniform(time.time(), end_time)
    
    # Blubbo is available to sing until timeout
    #while(time.time() < end_time):
        #logging.debug('elapsed time:')
        #logging.debug(time.time()-start_time)
        #logging.debug('next fart scheduled for:')
        #logging.debug(next_fart)
        #logging.debug('talk state')
        #logging.debug(talk_state)
        #if not mouth_event.isSet():
    song_num = random.randint(0,3)
    sing_song(song_num)
#     mouth_event.wait()
    # time.sleep(10)
        # when it's time to fart he farts
        #if time.time() >= next_fart:
            #make_fart()
            #time.sleep(2)
            #next_fart = random.uniform(time.time(), end_time)
    
    # say goodbye
    say_stuff(1)    
    # wait to say goodbye until done singing
    logging.debug('joining threads')
    mouth.do_run = False
    mouth.join()
   # eyes.join()
    logging.debug('threads are joined')
    
