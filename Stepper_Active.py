from time import sleep
import RPi.GPIO as gpio

DIR = 20   # CW
STEP = 21  # CLK
CW =1    
CCW =0

gpio.setmode(gpio.BCM)
gpio.setup(DIR, gpio.OUT)
gpio.setup(STEP, gpio.OUT)
# gpio.output(DIR,CW)



angle = 50
pulse = int(angle /1.8)

def TYPE_1():
    gpio.output(DIR, CW)
    global pulse
    for i in range(pulse):
        gpio.output(STEP,gpio.HIGH)
        sleep(.0010)
        gpio.output(STEP,gpio.LOW)
        sleep(.0010)

    gpio.output(DIR, CCW)
    for x in range(pulse):
        gpio.output(STEP,gpio.HIGH)
        sleep(.0010)
        gpio.output(STEP,gpio.LOW)
        sleep(.0010)


def TYPE_2():
    gpio.output(DIR, CCW)
    global pulse
    for i in range(pulse):
        gpio.output(STEP,gpio.HIGH)
        sleep(.0010)
        gpio.output(STEP,gpio.LOW)
        sleep(.0010)

    gpio.output(DIR, CW)
    for x in range(pulse):
        gpio.output(STEP,gpio.HIGH)
        sleep(.0010)
        gpio.output(STEP,gpio.LOW)
        sleep(.0010)


# TYPE_2(alpha=pulse)
