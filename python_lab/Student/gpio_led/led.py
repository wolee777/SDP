# 01 led ex

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led_pin1 = 14 
led_pin2 = 15

GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

try:
	while True:
		GPIO.output(led_pin1, False)
		GPIO.output(led_pin2, False)
		time.sleep(1)

		GPIO.output(led_pin1, True)
		GPIO.output(led_pin2, True)
		time.sleep(1)
finally:
	print("Cleaning up")
	GPIO.cleanup()
