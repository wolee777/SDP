import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings(False)

led1 = 14
led2 = 15

MOTOR_P = 4
MOTOR_N = 25
MOTOR_EN = 12

gpio = [ 5, 6, 16, 20, 21 ] # [ up, dn, lt, rt, cen ]
state = [ 0, 0, 0, 0, 0 ]

def led_init( led1, led2 ):
        GPIO.setup( led1, GPIO.OUT )
        GPIO.setup( led2, GPIO.OUT )

def led_on( led_pin ):
        GPIO.output( led_pin, True )

def led_off( led_pin ):
        GPIO.output( led_pin, False )

def motor_init():
    GPIO.setup( MOTOR_P, GPIO.OUT )
    GPIO.setup( MOTOR_N, GPIO.OUT )
    GPIO.setup( MOTOR_EN, GPIO.OUT )

def motor_forword():
    print( 'forword' )
    GPIO.output( MOTOR_P, True )
    GPIO.output( MOTOR_N, False )
    GPIO.output( MOTOR_EN, True )
    time.sleep( 1 )

def motor_backword():
    print( 'backword' )
    GPIO.output( MOTOR_P, False )
    GPIO.output( MOTOR_N, True )
    GPIO.output( MOTOR_EN, True )
    time.sleep( 1 )

def motor_stop():
    GPIO.output( MOTOR_EN, False )

def print_jog_all():
    print( 'up : {0}\tdown : {1}\tleft : {2}\tright : {3}\tcenter : {4}\t'.format( state[ 0 ],
    state[ 1 ], state[ 2 ], state[ 3 ], state[ 4 ] ) )

try:
    led_init( led1,led2 )
    led_off( led1 )
    led_off( led2 )

    motor_init()

    for i in range( 5 ):
        GPIO.setup( gpio[ i ], GPIO.IN )
    
    current_state = 0
    motor_state = 0

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
                elif i == 4:        # Center, stop program
                    led_off( led1 )
                    led_off( led2 )
                    GPIO.cleanup()
                    sys.exit()
                else :
                    print('Unknown')
                
                # up -> motor backword, down -> motor forword
                if i == 0 and state[ i ] == 1:
                    motor_backword()
                elif i == 1 and state[ i ] == 1:
                    motor_forword()
                else:
                    motor_stop()

finally:
    GPIO.cleanup()
    