import time

import RPi.GPIO as GPIO

FREQ = 120


##enable pins
#enablePinD = None 
#enablePinMLift = None
#enablePinMRot = None
#
##identify the right motor pins
#motorPinD = None
#motorPinMLift = None
#motorPinMRot = None
#
## as tuples just to reudce .setup lines
#pinDList = [enablePinD, motorPinD]
#pinMLList = [enablePinMLift, motorPinMLift]
#pinMRList = [enablePinMRot, motorPinMRot]
#
#pinList = [pinDList, pinMLList, pinMRList]
#
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(pinList, GPIO.OUT)

# Easier to set up all GPIO at once
from NASAcode.tools import setup_gpio as sg
sg.setup()

# https://www.pololu.com/product/2135

"""
Mode HIGH...
xIN1 = Phase pin = ON/OFF
xIN2 = Enable pin = Speed

(xIN1, xIN2)

(LOW, #) == forward @ #% speed
(HIGH, #) == backward @ #% speed

"""

"""

on drv,
phase, direction of the motor (high forward, low backwards)
enable, the speed of the motor (0 off, high 100%)


Parameters:
- pPin [int] - : Phase pin (actually enable) to turn the motor on/off
- ePin [int]: Enable pin (actually phase) to control the speed of the motor
- direction [char]: "F" or "B" for forward/right or backwards/left relatively
- intSped [int]: Starting speed of the motor, if no endSpd is specified is also the settled speed
- endSped [int]: Settling speed of the motor, 
"""
def motorON(pPin, ePin, direction, intSpd, endSpd = -1):
    global FREQ
    eSpeed = intSpd
    GPIO.output(ePin, 1)

    if (endSpd == -1):
        endSpd = intSpd

    if (direction == "F"):
        GPIO.output(pPin, 0)
        pwm = GPIO.PWM(ePin, FREQ)
        pwm.start(eSpeed)
    elif (direction == "B"):
        GPIO.output(pPin, 1)
        pwm = GPIO.PWM(ePin, FREQ)
        pwm.start(eSpeed)
    rampSpd(pwm, intSpd, endSpd)

def motorON2(dir_pin, pwm_pin, direction,speed=100):
    minPWM = 40 # Just a guess, might wanna play around with this and see what value works best.
    
    GPIO.output(dir_pin, direction)
    if(speed > 100):
        GPIO.output(pwm_pin, 1)
    elif(speed<minPWM): # Protect from stalling the motors at low voltages
        print("Speed submitted is below the min value")
        return False
    else:
        pwm = GPIO.PWM(pwm_pin, FREQ)
        pwm.start(minPWM)
        rampSpd(pwm, minPWM, speed)
    return True

def motorOff(ePin):
    GPIO.output(ePin, 0)

def rampSpd(pwm, startSpd, endSpd):
    if (endSpd > 100):
        endSpd = 100
    

    if (endSpd != -1):
        if (endSpd > startSpd):
            interval = round((endSpd - startSpd) / 9)
        else:
            interval = round((startSpd - endSpd) / 9)

    startSpd += interval
    endSpd += interval        

    for i in range(startSpd, endSpd, interval):
        if (i > 100):
            pwm.ChangeDutyCycle(100)
            break
        pwm.ChangeDutyCycle(i)
        time.sleep(0.5)

def cleanPins(pinList):
    GPIO.cleanup(pinList)

def run_test(enable, phase):
    pins = [enable, phase]            
    GPIO.output(pins, GPIO.HIGH)

     
def off(direction, pwm):
    pins = [direction, pwm]          

    GPIO.output(pins, GPIO.LOW)  