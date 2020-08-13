# lab05_motor
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_RP = 4
GPIO_RN = 25
GPIO_EN = 12


GPIO.setwarnings(False)


def motor_init():
        print ('init')
        GPIO.setup(GPIO_RP, GPIO.OUT)
        GPIO.setup(GPIO_RN, GPIO.OUT)
        GPIO.setup(GPIO_EN, GPIO.OUT)

def motor_forward():
        print ('forward')
        GPIO.output(GPIO_RP, True)
        GPIO.output(GPIO_RN, False)
        GPIO.output(GPIO_EN, True)

def motor_backward():
        print ('backward')
        GPIO.output(GPIO_RP, False)
        GPIO.output(GPIO_RN, True)
        GPIO.output(GPIO_EN, True)

def motor_stop():
        print ('stop')
        GPIO.output(GPIO_EN, False)

if __name__ == "__main__":
        motor_init()
        motor_forward()
        time.sleep(1)
        motor_stop()
        time.sleep(1)
        motor_backward()
        time.sleep(1)
        motor_stop()
        time.sleep(1)
        GPIO.cleanup()