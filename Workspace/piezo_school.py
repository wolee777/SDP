import RPi.GPIO as GPIO
import time

piezo = 13
hz = { 'do':261, 're':293.6648, 'mi':329.6276, 'fa':349.2282, 
       'sol':391.9954, 'ra':441.0000, 'si':493.8833 }
scores = ( 'sol', 'sol', 'ra', 'ra', 'sol', 'sol', 'mi', 'sol', 'sol', 'mi', 'mi', 're' )

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )
GPIO.setup( piezo, GPIO.OUT )

p = GPIO.PWM( piezo, 1.0 )
p.start( 90 )

try:
    for scale in scores:
         p.ChangeFrequency( hz[ scale ] )
         time.sleep( 0.5 )

except:
    print( 'Exception...' )
finally:
    p.stop()
    GPIO.cleanup()
