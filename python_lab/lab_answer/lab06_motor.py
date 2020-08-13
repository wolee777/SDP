# lab06_motor
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_RP = 4
GPIO_RN = 25
GPIO_EN = 12


GPIO.setwarnings(False)


def motor_init():
        print ('stop')
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

def motor_change_speed(p,duty):
        print ('change_speed')
        p.ChangeDutyCycle(duty)

if __name__ == "__main__":
        motor_init()
        motor_forward()
        p = GPIO.PWM(GPIO_EN, 100)
        p.start(0)

        while True:

            for duty in range(0,101,10):
                motor_change_speed(p,duty)
                print(duty)
                time.sleep(0.2)
                
            for duty in range(100,-1,-10):
                motor_change_speed(p,duty)
                print(duty)
                time.sleep(0.2)

            time.sleep(1)

        motor_stop()
        GPIO.cleanup()   
