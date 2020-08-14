import RPi.GPIO as GPIO
import time

piezo = 13
hz = ( 261, 6256, 293.6648, 329.6276, 349.2282, 391.9954, 441.0000, 493.8833, 523.2511 )

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )
GPIO.setup( piezo, GPIO.OUT )

p = GPIO.PWM( piezo, 1.0 )
p.start( 50 )

try:
    for n in hz:
            p.ChangeFrequency( n )
            time.sleep( 1 )
except:
    print( 'Exception...' )
finally:
    p.stop()
    GPIO.cleanup()
