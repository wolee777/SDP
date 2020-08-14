import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BCM )

MOTOR_P = 4
MOTOR_N = 25
MOTOR_EN = 12

GPIO.setup( MOTOR_P, GPIO.OUT )
GPIO.setup( MOTOR_N, GPIO.OUT )
GPIO.setup( MOTOR_EN, GPIO.OUT )

try:
    while True:
        print( 'forword' )
        GPIO.output( MOTOR_P, True )
        GPIO.output( MOTOR_N, False )
        GPIO.output( MOTOR_EN, True )
        time.sleep( 1 )

        print( 'stop' )
        GPIO.output( MOTOR_EN, False )
        time.sleep( 1 )

        print( 'backword' )
        GPIO.output( MOTOR_P, False )
        GPIO.output( MOTOR_N, True )
        GPIO.output( MOTOR_EN, True )

        print( 'stop' )
        GPIO.output( MOTOR_EN, False )
        time.sleep( 1 )
finally:
    GPIO.cleanup()
