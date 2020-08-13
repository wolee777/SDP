# lab04_jogsw
import RPi.GPIO as GPIO
import time

led1 = 14
led2 = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#gpio  [ up, dn, lt, rt, cen]
gpio = [  5,  6, 16, 20,  21]
#stat  [ up, dn, lt, rt, cen]
stat = [  0,  0,  0,  0,   0]

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

        cur_stat = 0

        while True:
            for i in range(5):
                cur_stat = GPIO.input(gpio[i])
                if cur_stat != stat[i]:
                    stat[i] = cur_stat
                    print_jog_all()
                    print (i)
                    
                    if i == 0:          # Up
                        led_off(led1)
                        led_on(led2)
                    
                    elif i == 1:        # Down  
                        led_on(led1)
                        led_off(led2)
                        
                    elif i == 2:        # Left
                        led_on(led1)
                        led_on(led2)
                        
                    elif i == 3:        # Right
                        led_off(led1)
                        led_off(led2)
                        
                    elif i == 4:        # Center
                        led_on(led1)
                        led_on(led2)
                        
                    else :
                        print('Unknown')
                        

    finally:
        print("Cleaning up")
        GPIO.cleanup()

