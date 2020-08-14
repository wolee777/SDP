import RPi.GPIO as GPIO
import time

trig = 0 # transmit
echo = 1 # receive

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )

GPIO.setup( trig, GPIO.OUT )
GPIO.setup( echo, GPIO.IN )

try:
    while True:
        GPIO.output( trig, False )
        time.sleep( 0.5 )

        GPIO.output( trig, True )
        time.sleep( 0.00001 )

        GPIO.output( trig, False )

        while GPIO.input( echo ) == False:
            pluse_start = time.time()
        
        while GPIO.input( echo ) == True:
            pluse_end = time.time()

        pluse_duration = pluse_end - pluse_start
        distance = pluse_duration * 17000
        distance = round( distance )

        print( 'Distance : {:.2f}cm'.format( distance ) )
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()