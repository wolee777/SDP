from bottle import route, run
import RPi.GPIO as GPIO
import datetime

import smbus
import time

GPIO.setmode(GPIO.BCM)
led_pins = [14, 15]
led_states = [0, 0]
btn_pin = 21        ## Jog SW center button
GPIO.setup(led_pins[0], GPIO.OUT)
GPIO.setup(led_pins[1], GPIO.OUT)
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

bus = smbus.SMBus(1)
addr = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe


def blink(pin_num):
    GPIO.output(pin_num, GPIO.HIGH) ## On 14
    time.sleep(1)
    GPIO.output(pin_num, GPIO.LOW)  ## off 14
    time.sleep(1)

    return

def btn_status():
    state = GPIO.input(btn_pin)
    if state:
        return 'Up'
    else:
        return 'Down'
def html_for_led(led):
    GPIO.output(led_pins[0],  GPIO.LOW) ## On 14
    l = str(led)
    result = "<input type='button' onClick='changed(" + l + ")' value='LED " + l + "'/>"
    return result
def update_leds():
    for i, value in enumerate(led_states):
        GPIO.output(led_pins[i], value)

@route('/')
@route('/<led>')
def index(led="n"):
    if led != "n":
        led_num = int(led)
        led_states[led_num] = not led_states[led_num]
        update_leds()
    # Temp and Humidity sensing
    temp1 = 0.0
    humi = 0.0
    val = 0
    data = [0, 0]
    resp = ""

    bus.write_byte (addr, soft_reset)
    time.sleep(0.05)

    while True:
	# temperature
	bus.write_byte(addr, cmd_temp)
	time.sleep(0.260)
	for i in range(0,2,1):
            data[i] = bus.read_byte(addr)

	val = data[0] << 8 | data[1]
	temp1 = -46.85+175.72/65536*val


	# humidity
	bus.write_byte(addr, cmd_humi)
	time.sleep(0.260)
		
	for i in range(0,2,1):
           data[i] = bus.read_byte(addr)

	val = data[0] << 8 | data[1]
	humi = -6.0+125.0/65536*val;
                
        THI = (temp1+humi)*0.72+40.2
	#print 'temp : %.2f, humi : %.2f, THI: %.2f' %(temp, humi, THI)
	time.sleep(1)

        if temp1>32.:
            resp = "It is very hot..!!"
        elif temp1<32. and temp1>30:
           resp = "It is  warm..!!"
        elif temp1<20:
           resp = "It is cold..!!"
        else:
           resp = "It is good..!!"
           
        response = "<script>"
        response += "function changed(led)"
        response += "{"
        response += " window.location.href='/' + led"
        response += "}"
        response += "</script>"
        response += '<h1>GPIO Control</h1>'
        response += '<h2>Button=' + btn_status() + '</h2>'
        response += '<h2>The current temperture of this room is ' + (str)(temp1) + ' degree</h2>'
        response += '<br>'
        response += '<h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + resp + '</h3>'
        response += '<br>'
        response += '<h2>LEDs</h2>'
        response += html_for_led(0)
        response += html_for_led(1)

        if temp1>32.:
            for i in range(0,5):
                blink(led_pins[0])
                
        return response

        

run(host='0.0.0.0', port=8080)
