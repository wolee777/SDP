import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#gpio  [ up, dn, lt, rt, cen]
gpio = [  5,  6, 16, 20,  21]
#stat  [ up, dn, lt, rt, cen]
stat = [  0,  0,  0,  0,   0]

def print_jog_all():
	print ('up : %d, down: %d, left: %d, right : %d, cen: %d'\
		%(stat[0], stat[1], stat[2], stat[3], stat[4]))

try:
	for i in range(5):
		GPIO.setup(gpio[i], GPIO.IN)

	cur_stat = 0

	while True:
		for i in range(5):
			cur_stat = GPIO.input(gpio[i])
			if cur_stat != stat[i]:
				stat[i] = cur_stat
				print_jog_all()

finally:
	print("Cleaning up")
	GPIO.cleanup()
