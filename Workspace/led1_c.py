# led1.py
import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BCM ) # GPIO 초기화 ( 모드 설정 )

led_pin1 = 14
led_pin2 = 15
# GPIO핀 동작 설정
GPIO.setup( led_pin1, GPIO.OUT )
GPIO.setup( led_pin2, GPIO.OUT )

try:
    while True:
        GPIO.output( led_pin1, False ) # Low값 전송
        GPIO.output( led_pin2, False )
        time.sleep( 1 )
        GPIO.output( led_pin1, True ) # High값 전송
        GPIO.output( led_pin2, True )
        time.sleep( 1 )
finally:
    print( 'stop program' )
    GPIO.cleanup() # GPIO 정리
