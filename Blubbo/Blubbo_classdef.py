import logging
import RPi.GPIO as GPIO
import time
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Blubbo:
    'Things that Blubbo can do'
    
    def __init__(self):
        # all the sounds that are associated with Blubbo
        
        # fart sounds
        self.fart = ["fart1.mp3", "fart2.mp3", "fart3.mp3", "fart4.mp3", "fart5.mp3", "fart6.mp3", "fart7.mp3"]
        
        # songs he currently knows how to sing
        self.song = ["ILRNR.mp3", "You_shook_me.mp3", "Beatles_birthday.mp3", "GummyBear.mp3"]
        
        # talk is array of things he can say: a greeting and a goodbye
        self.talk = ['greet','goodbye']
        self.talk[0] = "My name is Blubbo. I am a fish. I like to sing. If you touch my fin, I will sing for you"
        self.talk[1] = "It was great to sing and play today. Goodbye"
        
    def eyes_off(self, r,g,b):
        # All eye colors off
        GPIO.output(r, False)
        GPIO.output(g, False)
        GPIO.output(b, False)
        
    def eyes_on(self, r,g,b):
        # Natural eye on state
        GPIO.output(r,False)
        GPIO.output(g,True)
        GPIO.output(b,True)
        
    def blink(self, blink_type, r, g, b):
        # blink a different pattern depending on the blink_type
        
        # blink between off and blue green
        if blink_type == 1:
            logging.debug('blink_type is 1')
            GPIO.output(r, False)
            GPIO.output(g, True)
            GPIO.output(b, True)
            logging.debug('green and blue eyes on and bright')
            time.sleep(0.2)
            self.eyes_off(r,g,b)
            logging.debug('both eyes off')
            time.sleep(1)
            GPIO.output(r, False)
            GPIO.output(g, True)
            GPIO.output(b, True)
            time.sleep(1)
            self.eyes_off(r,g,b)
            
        # blink between off and red and blue
        elif blink_type == 2:
            logging.debug('blink_type is 2')
            GPIO.output(r, True)
            GPIO.output(g, False)
            GPIO.output(b, False)
            time.sleep(0.2)
            self.eyes_off(r,g,b)
            time.sleep(0.3)
            GPIO.output(r, False)
            GPIO.output(b, True)
            GPIO.output(g, False)
            time.sleep(0.2)
            self.eyes_off(r,g,b)
            
        # fast red eye blinking
        elif blink_type == 3:
            logging.debug('blink_type is 3')
            GPIO.output(r, True)
            GPIO.output(g, False)
            GPIO.output(b, False)
            time.sleep(0.2)
            self.eyes_off(r,g,b)
            time.sleep(0.3)
            GPIO.output(r, True)
            GPIO.output(b, False)
            GPIO.output(g, False)
            time.sleep(0.1)
            self.eyes_off(r,g,b)
            
        # blink between green and magenta
        elif blink_type == 4:
            logging.debug('blink_type is 4')
            GPIO.output(r, False)
            GPIO.output(g, True)
            GPIO.output(b, False)
            time.sleep(0.4)
            self.eyes_off(r,g,b)
            time.sleep(1)
            GPIO.output(r, True)
            GPIO.output(b, True)
            GPIO.output(g, False)
            time.sleep(0.6)
            self.eyes_off(r,g,b)
            
    def move_mouth(self, servoPIN):
        GPIO.setup(servoPIN, GPIO.OUT)
        p = GPIO.PWM(servoPIN, 50)  # sets PWM to frequency of 50 Hz
        for i in range(4):
            p.start(99) # initialization to 2.5% of duty cycle
            # why did I choose 2.5? 
            time.sleep(random.randint(15,60)/150.0)
            p.ChangeDutyCycle(8)
            time.sleep(random.randint(15,60)/150.0)
            p.ChangeDutyCycle(10)
            time.sleep(random.randint(15,60)/150.0)
            p.ChangeDutyCycle(13)
            time.sleep(random.randint(15,60)/150.0)
            p.ChangeDutyCycle(15)
            p.ChangeDutyCycle(13.5)
            time.sleep(random.randint(15,60)/150.0)
            p.ChangeDutyCycle(11)
            time.sleep(random.randint(15,60)/150.0)
            p.ChangeDutyCycle(9.5)
            time.sleep(random.randint(15,60)/150.0)
            p.ChangeDutyCycle(8)
            time.sleep(1)
        p.stop()
