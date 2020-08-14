import RPi.GPIO as GPIO
import time

pir = 24

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )
GPIO.setup( pir, GPIO.IN )

def loop():
    cnt = 0
    while True:
        if ( GPIO.input( pir ) == True ):
            print( 'detected {}'.format( cnt ) )
            cnt += 1
        time.sleep( 0.1 )

try:
    loop()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    