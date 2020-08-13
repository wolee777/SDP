from flask import Flask, render_template
import datetime
import RPi.GPIO as GPIO

import smbus
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
led_pins = [14, 15]
led_states = [0, 0]
GPIO.setup(led_pins[0], GPIO.OUT)
GPIO.setup(led_pins[1], GPIO.OUT)

bus = smbus.SMBus(1)
addr = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe


def html_for_led(led):
    l = str(led)
    result = "<input type='button' onClick='changed(" + l + ")' value='LED " + l + "'/>"
    return result
def update_leds():
    for i, value in enumerate(led_states):
        GPIO.output(led_pins[i], value)

@app.route("/")
@app.route('/<led>')
def index(led="n"):

   if led != "n":
        led_num = int(led)
        led_states[led_num] = not led_states[led_num]
        update_leds()
   response = "<script>"
   response += "function changed(led)"
   response += "{"
   response += " window.location.href='/' + led"
   response += "}"
   response += "</script>"
   response += '<h2>LEDs</h2>'
   response += html_for_led(0)
   response += html_for_led(1)
    
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")

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

       if temp1>30.:
          resp = "It is so warm..!!"
       elif temp1<20:
          resp = "It is cold..!!"
       else:
          resp = "It is good..!!"

        
       templateData = {
            'title' : 'TEST-3',
            'time': timeString,
            'temp': temp1,
            'msg': resp,
            'led_btn': response
            }
       return render_template('main.html', **templateData)

   
@app.route("/readPin/<pin>")
def readPin(pin):
   try:
      GPIO.setup(int(pin), GPIO.IN)
      if GPIO.input(int(pin)) == True:
         response = "Pin number " + pin + " is high!"
      else:
         response = "Pin number " + pin + " is low!"
   except:
      response = "There was an error reading pin " + pin + "."

   templateData = {
      'title' : 'Status of Pin' + pin,
      'response' : response
      }

   return render_template('pin.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
