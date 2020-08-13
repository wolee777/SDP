import RPi.GPIO as GPIO 
import time 

GPIO.setmode(GPIO.BCM)
gpio_pin=13
GPIO.setup(gpio_pin, GPIO.OUT) 

try:

	scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]
	scale2 = [ 1047, 1175, 1319, 1397, 1568, 1760, 1976, 2093 ]
	p = GPIO.PWM(gpio_pin, 100)
	GPIO.output(gpio_pin, True) 
	p.start(100) # start the PWM on 100% duty cycle  
	p.ChangeDutyCycle(90) # change the duty cycle to 90%  

	for i in range(8): 
		print (i+1) 
		p.ChangeFrequency(scale2[i]) 
		time.sleep(1) 
	
	p.stop()   # stop the PWM output  

finally:
	GPIO.cleanup()
