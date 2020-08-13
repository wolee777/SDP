# lab02_led

import RPi.GPIO as GPIO
import time

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
        p = GPIO.PWM(led1, 100)
        p.start(0)

        while True:
            for duty in range(0,101,5):
                p.ChangeDutyCycle(duty)
                print(duty)
                time.sleep(0.1)
                
            for duty in range(100,-1,-5):
                p.ChangeDutyCycle(duty) 
                print(duty)
                time.sleep(0.1) 
    
  