#!/user/bin/env python3
# Code is inspired by Arduino CapacitiveSensor Library,
# Modified from Emeric Florence's version which is available here:
# https://bitbucket.org/boblemarin/raspberrypi-capacitive-sensor/src/1c18fad88ae70ce1d83dee9c43528e27664a150d/CapSense1/CapSenseAndLEDs.py?at=master

import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def CapRead(inPin,outPin):
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

def main():
    inPin = 16
    outPin = 12
    for x in range (0,1900):
        level = CapRead(inPin, outPin)
        print('level')
        print(level)
        if level > 20:
            print('sensed')
        time.sleep(0.1)
    
if __name__=="__main__":
    main()
    
# clean before you leave
GPIO.cleanup()
