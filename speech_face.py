#!/usr/bin/python3
# in this program the puppet talks, recognizes user voice
# and moves eyes and mouth

import subprocess
import RPi.GPIO as GPIO
import time
import threading # read https://realpython.com/intro-to-python-threading/
import logging # info about how to use logging at https://realpython.com/python-logging/

logging.basicConfig(level=logging.DEBUG)
logging.debug('This will get logged')

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
    subprocess.call('espeak -s 100 -v en-uk-north "I am a puppet and who are you?" --stdout | aplay', shell=True)
    subprocess.call('espeak -s 100 -v sw "Mimi ni kidoli. wewe ni nani? " --stdout | aplay', shell=True)
    subprocess.call('espeak -s 100 -v es "Yo soy una muneca. Quien eres tu?" --stdout | aplay', shell=True)

def blink_eyes(blink_type):
    if blink_type==1:
        GPIO.output(g_eye,True)
        GPIO.output(blue_eye,True)
        time.sleep(1)
        GPIO.output(g_eye,False)
        GPIO.output(b_eye,False)
    else:
        for i in range(4):
            GPIO.output(g_eye,True)
            GPIO.output(b_eye,False)
            time.sleep(1)
            GPIO.output(b_eye,True)
            GPIO.output(g_eye,False)
            time.sleep(0.7)

def move_mouth():
    p = GPIO.PWM(servoPIN, 50)
    p.start(2.5) # initialization
    talking = speak.empty()# check to see if the puppet should be talking
    while (talking ==True):
        # need a while talking. do i need the try?
        p.ChangeDutyCycle(3)
        time.sleep(0.2)
        p.ChangeDutyCycle(7.5)
        p.ChangeDutyCycle(6)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(2.5)
        talking = talkthread.Event()
    p.stop()
    GPIO.cleanup()

# would I be able to check whether other threads were started and ended if
# I didn't start them from main?
# speech output and mouth movement at same time
greet = threading.Thread(target=say_greetings)
speak = threading.Thread(target=move_mouth)

def main():

    #blink = threading.Thread(target=blink_eyes,args=1)
    greet.start()
    speak.start()
    #blink.start()
    time.sleep(15)

if __name__=="__main__":
    main()
