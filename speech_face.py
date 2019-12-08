#!/usr/bin/python3
# in this program the puppet talks, asks the user their name, and says hi
# mouth moves, eyes blink
# because Raspi doesn't have microphone jack, user inputs name on the keyboard

import subprocess
import RPi.GPIO as GPIO
import time
import threading # read https://realpython.com/intro-to-python-threading/
import logging # info about how to use logging at https://realpython.com/python-logging/
import sys


logging.basicConfig(level=logging.DEBUG)
logging.debug('Starting the program')
logging.debug('python version ' + sys.version)

# set up GPIO settings and pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
g_eye = 17
b_eye =15
servoPIN = 18
GPIO.setup(g_eye,GPIO.OUT)
GPIO.setup(b_eye,GPIO.OUT)
GPIO.setup(servoPIN, GPIO.OUT)

def say_greetings():
    greet_event.set()  # thought I'd need the events actually probably dont
    logging.debug('starting saying the greetings')
    subprocess.call('espeak -s 100 -v en-uk-north "I am a puppet and who are you?" --stdout | aplay', shell=True)
    subprocess.call('espeak -s 100 -v sw "Mimi ni kidoli. wewe ni nani? " --stdout | aplay', shell=True)
    subprocess.call('espeak -s 100 -v es "Yo soy una muneca. Quien eres tu?" --stdout | aplay', shell=True)
    logging.debug('finished saying greetings')
    greet_event.clear()

def get_uname():
    # need this to be global so that it will be available to say_stuff function
    try:
        uname = input('Enter your name here then hit return\n')
        logging.debug('got user name')
        return uname
    except:
        logging.debug('did not get user name')
        return 1

def say_stuff():
    logging.debug('talking to the user')
    try:
        if isinstance(uname,str):
            text = "So nice to meet you"+uname
        else:
            logging.debug('user input not recognized')
            text = "Sorry I didn't understand you. It's nice to meet you anyways."
        subprocess.call('espeak -s 100 -v en-uk-north "%s" --stdout | aplay'%text, shell=True)
    except:
        text = "Sorry I didn't understand you. It's nice to meet you anyways."
        subprocess.call('espeak -s 100 -v en-uk-north "%s" --stdout | aplay'%text, shell=True)
    logging.debug('finished speaking')

def blink_eyes():
    blink_type=1
    keep_blinking = greet.isAlive()
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
    else:
        for i in range(4):
            GPIO.output(g_eye,True)
            GPIO.output(b_eye,False)
            time.sleep(1)
            GPIO.output(b_eye,True)
            GPIO.output(g_eye,False)
            time.sleep(0.7)
        GPIO.output(b_eye,False)

def move_mouth(talk_func_name):
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
    global uname
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