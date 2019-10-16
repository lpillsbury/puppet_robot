#!/usr/bin/python3
# in this program the puppet talks, recognizes user voice
# and moves eyes and mouth

import subprocess
import RPi.GPIO as GPIO
import time
import threading # read https://realpython.com/intro-to-python-threading/
import logging # info about how to use logging at https://realpython.com/python-logging/

logging.basicConfig(level=logging.DEBUG)
logging.debug('Starting the program')

# set up GPIO settings and pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
g_eye = 18
b_eye =15
servoPIN =17
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
    
def say_stuff(uname):
    logging.debug('talking to the user')
    if isinstance(uname,str):
        text = "So nice to meet you"+uname
    else:
        text = "Sorry I didn't understand you. It's nice to meet you anyways."
    
    subprocess.call('espeak -s 100 -v en-uk-north text --stdout | aplay', shell=True)
    logging.debug('finished speaking')
    
def blink_eyes():
    blink_type=2
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
    p = GPIO.PWM(servoPIN, 50)
    logging.debug('starting to move the mouth')
    p.start(2.5) # initialization
    
    # puppet will only move its mouth when it says words
    keep_talking = talk_func_name.isAlive()
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
        keep_talking = greet.isAlive()
        logging.debug('keep talking=')
        logging.debug(keep_talking)
    talk_func_name.join()
    p.stop()
    GPIO.cleanup()
    logging.debug('Done moving mouth')

# would I be able to check whether other threads were started and ended if
# I didn't start them from main?
# speech output and mouth movement at same time
greet = threading.Thread(target=say_greetings)
yap1 = threading.Thread(target=move_mouth, args='greet')
yap2 = threading.Thread(target=move_mouth, args='say_stuff')
greet_event = threading.Event()
blink = threading.Thread(target=blink_eyes)
say_stuff = threading.Thread(target=say_stuff, args="Leah")

def main():
    greet.start()
    yap1.start()
    blink.start()
    yap1.join()
    blink.join()
    
    # will now say hello
    yap2.start()
    say_stuff.start()
    yap2.join()
    logging.debug('program has ended')
 
if __name__=="__main__":
    main()
