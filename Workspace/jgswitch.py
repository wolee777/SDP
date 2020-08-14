import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BCM )

gpio = [ 5, 6, 16, 20, 21 ] # [ up, dn, lt, rt, cen ]
state = [ 0, 0, 0, 0, 0 ]

def print_jog_all():
    print( 'up : {0}\tdown : {1}\tleft : {2}\tright : {3}\tcenter : {4}\t'.format( state[ 0 ],
    state[ 1 ], state[ 2 ], state[ 3 ], state[ 4 ] ) )

try:
    for i in range( 5 ):
        GPIO.setup( gpio[ i ], GPIO.IN )
    
    current_state = 0

    while True:
        for i in range( 5 ):
            current_state = GPIO.input( gpio[ i ] )
            if current_state != state[ i ]:
                state[ i ] = current_state
                print_jog_all()
finally:
    GPIO.cleanup()
    