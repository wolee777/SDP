import RPi.GPIO as GPIO
import time
import led2 as LED
import clcd as CLCD

LED1 = 50
LED1_2 = 30
LED_BLINK = 10

trig = 0 # transmit
echo = 1 # receive

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )

GPIO.setup( trig, GPIO.OUT )
GPIO.setup( echo, GPIO.IN )

LED.led_init( LED.led1, LED.led2 )
LED.led_off( LED.led1 )
LED.led_off( LED.led2 )

CLCD.lcd_setup()
CLCD.lcd_init()

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

        print( 'Dist : {:6.2f}cm'.format( distance ) )
        
        message = 'Dist : {:6.2f}cm'.format( distance )
        CLCD.lcd_string( message, CLCD.LCD_LINE_1 )

        if distance <= LED_BLINK:
            LED.led_all_blink()
        elif distance <= LED1_2:
            LED.led_on( LED.led1 )
            LED.led_on( LED.led2 )
        elif distance <= LED1:
            LED.led_on( LED.led1 )
            LED.led_off( LED.led2 )
        else:
            LED.led_off( LED.led1 )
            LED.led_off( LED.led2 )
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()