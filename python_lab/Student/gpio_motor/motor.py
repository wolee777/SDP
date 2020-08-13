import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_RP = 4
GPIO_RN = 25
GPIO_EN = 12

GPIO.setup(GPIO_RP, GPIO.OUT)
GPIO.setup(GPIO_RN, GPIO.OUT)
GPIO.setup(GPIO_EN, GPIO.OUT)

try:
	while True:
		print ('forword')

		GPIO.output(GPIO_RP, True)
		GPIO.output(GPIO_RN, False)
		GPIO.output(GPIO_EN, True)
		time.sleep(1)

		print ('stop')
		GPIO.output(GPIO_EN, False)
		time.sleep(1)

		print ('backword')
		GPIO.output(GPIO_RP, False)
		GPIO.output(GPIO_RN, True)
		GPIO.output(GPIO_EN, True)
		time.sleep(1)

		print ('stop')
		GPIO.output(GPIO_EN, False)
		time.sleep(1)

finally:	
	GPIO.cleanup()
