#!/usr/bin/python3
# in this program the puppet talks, recognizes user voice
# and moves eyes and mouth

import subprocess
import RPi.GPIO as GPIO
import time
import threading

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
    try:
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
        p.stop()
        GPIO.cleanup()
        
    # this exception should actually be "when I'm done talking"
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
        
def main():
    # speech output and mouth movement at same time
    thread.start_new_thread(say_greetings,())
    thread.start_new_thread(move_mouth, ())
    time.sleep(10)
    #say_greetings()
    #move_mouth()
    #blink_eyes(1)
    
if __name__=="__main__":
    main()
