# led2.py
import RPi.GPIO as GPIO
import time

led1 = 14
led2 = 15

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )

def led_init( led1, led2 ):
    GPIO.setup( led1, GPIO.OUT )
    GPIO.setup( led2, GPIO.OUT )

def led_on( led_pin ):
    GPIO.output( led_pin, True )

def led_off( led_pin ):
    GPIO.output( led_pin, False )

def led_blink( led_pin, delay ):
    led_on( led_pin )
    time.sleep( delay )
    led_off( led_pin )
    time.sleep( delay )

def led_all_blink():
    led_on( led1 )
    led_on( led2 )
    time.sleep( 0.5 )
    led_off( led1 )
    led_off( led2 )
    time.sleep( 0.5 )

def led_shift( led1, led2, delay ):
    led_on( led1 )
    led_off( led2 )
    time.sleep( delay )
    led_on( led2 )
    led_off( led1 )
    time.sleep( delay )

if __name__ == "__main__":
    led_init( led1, led2 )
    led_on( led1 )
    time.sleep( 1 )
    led_on( led2 )
    time.sleep( 1 )
    led_off( led1 )
    time.sleep( 1 )
    led_off( led2 )
    time.sleep( 1 )
    led_blink( led1, 1 )
    led_blink( led2, 1 )
    led_shift( led1, led2, 2 )

    led_off( led1 )
    led_off( led2 )