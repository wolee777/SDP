import RPi.GPIO as GPIO
import time
import led2 as LED

pir = 24

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )
GPIO.setup( pir, GPIO.IN )

LED.led_init( LED.led1, LED.led2 )
LED.led_off( LED.led1 )
LED.led_off( LED.led2 )

def loop():
    cnt = 0
    while True:
        if ( GPIO.input( pir ) == True ):
            print( 'detected {}'.format( cnt ) )
            cnt += 1
            LED.led_on( LED.led1 )
        else:
            LED.led_off( LED.led1 )
            
        time.sleep( 0.1 )

try:
    loop()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    