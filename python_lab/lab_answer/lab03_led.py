# lab03_led

import RPi.GPIO as GPIO
import time
import random

led1 = 14
led2 = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def led_init(led1,led2):
    GPIO.setup(led1, GPIO.OUT)
    GPIO.setup(led2, GPIO.OUT)

def led_on(led_pin):
    GPIO.output(led_pin, True)

def led_off(led_pin):
    GPIO.output(led_pin, False)


if __name__ == "__main__":
    led_init(led1,led2)
    random.seed(None, 2)

    while True:
        led_pin = random.randint(14,15)  # random integer from 14 to 15
        print(led_pin)
        led_on(led_pin)
        led_off(led_pin^0x01)   # change led_pin  14-->15 , 15-->14
        time.sleep(0.1)
