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
GPIO.setmode(GPIO.BCM)

# red, green, blue eye pins, servo pin, right/left capacitive sensors

r_eye = 17
g_eye = 27
b_eye = 22
servoPIN = 18
capR = 24
capL = 23
# define the capacitive sensor pins here or in function?
# is function in this code or separate?

GPIO.setup(g_eye,GPIO.OUT)
GPIO.setup(b_eye,GPIO.OUT)
GPIO.setup(r_eye,GPIO.OUT)
GPIO.setup(capR, GPIO.OUT)
GPIO.setup(capL, GPIO.OUT)
GPIO.setup(servoPIN, GPIO.OUT)

def say_greeting():
    logging.debug('starting saying greeting')
    text = "My name is Blubbo. I am a fish. I like to sing. If you touch my fin, I will sing for you"
    subprocess.call('espeak -s 100 -v en "%s" --stdout | aplay'%text, shell=True)
    logging.debug('finished saying greeting')

def fart():
    # https://raspberrypi.stackexchange.com/questions/7088/playing-audio-files-with-python
    logging.debug('farting again')
    which_fart = random.randint(1,8)
    fname = 'fart' + which_fart + '.mp3'
    # subprocess.call(aplay fname)
    logging.debug('done farting')
   
def sing():
    logging.debug('singing')

def blink_eyes():
    blink_type=random.randint(1,5)
    keep_blinking = fart.isAlive()
    if blink_type==1:
        while(keep_blinking == True):
            GPIO.output(g_eye,True)
            GPIO.output(b_eye,True)
            logging.debug('both eyes on and bright')
            time.sleep(2)
            GPIO.output(g_eye,False)
            GPIO.output(b_eye,False)
            logging.debug('both eyes off')
            time.sleep(2)
            keep_blinking = greet.isAlive()
    elif blink_type ==2:
        for i in range(4):
            GPIO.output(g_eye,True)
            GPIO.output(b_eye,False)
            time.sleep(1)
            GPIO.output(b_eye,True)
            GPIO.output(g_eye,False)
            time.sleep(0.7)
        GPIO.output(b_eye,False)
    elif blink_type ==3 # etc etc how many choices do I want

def move_mouth(func_name):
    # Blubbo will move his mouth when singing or introducing himself
    p = GPIO.PWM(servoPIN, 50)  # sets PWM to frequency of 50 Hz
    logging.debug('moving mouth in accordance with speech in:')
    logging.debug(talk_func_name)
    p.start(2.5) # initialization to 2.5% of duty cycle
    # why did I choose 2.5? 
    
    # puppet will only move its mouth when it says words
    keep_talking = talk_func_name.isAlive()
    logging.debug('keep talking=')
    logging.debug(keep_talking)
    while (keep_talking==True):
        p.ChangeDutyCycle(3)
        time.sleep(0.2)
        p.ChangeDutyCycle(7.5)
        p.ChangeDutyCycle(6)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(2.5)
        logging.debug('Moved mouth a cycle')
        keep_talking = talk_func_name.isAlive()
        logging.debug('keep talking=')
        logging.debug(keep_talking)
    talk_func_name.join()
    p.stop()
    logging.debug('Done moving mouth')

greet = threading.Thread(target=say_greetings)
say_more = threading.Thread(target=say_stuff)
yap1 = threading.Thread(target=move_mouth, args=(greet,))
yap2 = threading.Thread(target=move_mouth, args=(say_more,))
greet_event = threading.Event()
blink = threading.Thread(target=blink_eyes)


def main():
    # overlaid in all of this, we have the cap sensor saying when to do it and time elapsed ff
    greet.start()
    yap1.start()
    blink.start()
    yap1.join()
    blink.join()
    uname = get_uname()
    # will now say hello
    time.sleep(2)
    logging.debug('will now respond')
    yap2.start()
    
    say_more.start()
    yap2.join()
 
if __name__=="__main__":
    main()

