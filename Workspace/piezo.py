import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )
piezo = 13
GPIO.setup( piezo, GPIO.OUT )

try:
    scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]
    scale2 = [ 1047, 1175, 1319, 1397, 1568, 1761, 1976, 2093 ]

    p = GPIO.PWM( piezo, 100 )
    GPIO.output( piezo, True )
    p.start( 100 )
    p.ChangeDutyCycle( 90 )

    for i in range( 8 ):
        print( i + 1 )
        p.ChangeFrequency( scale2[ i ] )
        time.sleep( 1 )
    p.stop()
finally:
    GPIO.cleanup()
