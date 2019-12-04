import RPi.GPIO as GPIO
import time
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

servoPIN = 18
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)  # sets PWM to frequency of 50 Hz
for i in range(4):
    p.start(99) # initialization to 2.5% of duty cycle
    # why did I choose 2.5? 
    time.sleep(random.randint(15,60)/150.0)
    #p.ChangeDutyCycle(9)
    time.sleep(random.randint(15,60)/150.0)
    p.ChangeDutyCycle(8)
    time.sleep(random.randint(15,60)/150.0)
    p.ChangeDutyCycle(13)
    time.sleep(random.randint(15,60)/150.0)
    p.ChangeDutyCycle(15)
    p.ChangeDutyCycle(13.5)
    time.sleep(random.randint(15,60)/150.0)
    p.ChangeDutyCycle(11)
    time.sleep(random.randint(15,60)/150.0)
    p.ChangeDutyCycle(8)
    time.sleep(random.randint(15,60)/150.0)
    #p.ChangeDutyCycle(9)
    time.sleep(1)
p.stop()
