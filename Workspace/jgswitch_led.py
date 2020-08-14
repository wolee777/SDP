import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings(False)

led1 = 14
led2 = 15

gpio = [ 5, 6, 16, 20, 21 ] # [ up, dn, lt, rt, cen ]
state = [ 0, 0, 0, 0, 0 ]

def led_init( led1, led2 ):
        GPIO.setup( led1, GPIO.OUT )
        GPIO.setup( led2, GPIO.OUT )

def led_on( led_pin ):
        GPIO.output( led_pin, True )

def led_off( led_pin ):
        GPIO.output( led_pin, False )

def print_jog_all():
    print( 'up : {0}\tdown : {1}\tleft : {2}\tright : {3}\tcenter : {4}\t'.format( state[ 0 ],
    state[ 1 ], state[ 2 ], state[ 3 ], state[ 4 ] ) )

try:
    led_init( led1,led2 )
    led_off( led1 )
    led_off( led2 )

    for i in range( 5 ):
        GPIO.setup( gpio[ i ], GPIO.IN )
    
    current_state = 0

    while True:
        for i in range( 5 ):
            current_state = GPIO.input( gpio[ i ] )
            if current_state != state[ i ]:
                state[ i ] = current_state
                print_jog_all()
                print (i)
                if i == 0:          # Up
                    led_off( led1 )
                    led_on( led2 )
                elif i == 1:        # Down  
                    led_on( led1 )
                    led_off( led2 )
                elif i == 2:        # Left
                    led_on( led1 )
                    led_on( led2 )
                elif i == 3:        # Right
                    led_off( led1 )
                    led_off( led2 )
                elif i == 4:        # Center
                    led_on( led1 )
                    led_on( led2 )
                else :
                    print('Unknown')

finally:
    GPIO.cleanup()
    