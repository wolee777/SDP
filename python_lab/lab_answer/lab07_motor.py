# lab07_motor
import RPi.GPIO as GPIO
import time

led1 = 14
led2 = 15

GPIO_RP = 4
GPIO_RN = 25
GPIO_EN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#gpio  [ up, dn, lt, rt, cen]
gpio = [  5,  6, 16, 20,  21]
#stat  [ up, dn, lt, rt, cen]
stat = [  0,  0,  0,  0,   0]


def motor_init():
        print ('init')
        GPIO.setup(GPIO_RP, GPIO.OUT)
        GPIO.setup(GPIO_RN, GPIO.OUT)
        GPIO.setup(GPIO_EN, GPIO.OUT)

def motor_forward():
        print ('forward')
        GPIO.output(GPIO_RP, True)
        GPIO.output(GPIO_RN, False)
        #GPIO.output(GPIO_EN, True)

def motor_backward():
        print ('backward')
        GPIO.output(GPIO_RP, False)
        GPIO.output(GPIO_RN, True)
        #GPIO.output(GPIO_EN, True)

def motor_stop():
        print ('stop')
        GPIO.output(GPIO_EN, False)

def motor_change_speed(p,duty):
        print ('change_speed :',duty)
        p.ChangeDutyCycle(duty)

def led_init(led1,led2):
        GPIO.setup(led1, GPIO.OUT)
        GPIO.setup(led2, GPIO.OUT)

def led_on(led_pin):
        GPIO.output(led_pin, True)

def led_off(led_pin):
        GPIO.output(led_pin, False)


def print_jog_all():
	print ('up : %d, down: %d, left: %d, right : %d, cen: %d'\
		%(stat[0], stat[1], stat[2], stat[3], stat[4]))


if __name__ == "__main__":
    try:
        for i in range(5):
            GPIO.setup(gpio[i], GPIO.IN)

        led_init(led1,led2)

        motor_init()

        cur_stat = 0

        p = GPIO.PWM(GPIO_EN, 100)
        p.start(0)

        m_speed = 0.0
        motor_change_speed(p,m_speed)
        
        while True:
            
            for i in range(5):
                cur_stat = GPIO.input(gpio[i])
                if cur_stat != stat[i]:
                    stat[i] = cur_stat
                    print_jog_all()
                    print (i)
                    
                    if i == 0:          # Up  : Motor speed Up
                        led_off(led1)
                        led_on(led2)
                        m_speed +=  0.5
                        if (m_speed > 10):
                            m_speed = 10
                        motor_change_speed(p,m_speed*10)                            
                                            
                    elif i == 1:        # Down  : Motor speed Down
                        led_on(led1)
                        led_off(led2)
                        m_speed -=  0.5
                        if (m_speed < 0):
                            m_speed = 0                        
                        motor_change_speed(p,m_speed*10)
                                                    
                    elif i == 2:        # Left  : Motor Forward
                        led_on(led1)
                        led_on(led2)
                        motor_forward()
                        
                    elif i == 3:        # Right : Motor Backward
                        led_off(led1)
                        led_off(led2)
                        motor_backward()
                        
                    elif i == 4:        # Center : Motor Stop
                        led_on(led1)
                        led_on(led2)
                        #motor_stop()
                        m_speed =  0
                        motor_change_speed(p,m_speed)
                        
                    else :
                        print('Unknown')                        

    finally:
        p.stop()
        print("Cleaning up")
        GPIO.cleanup()

