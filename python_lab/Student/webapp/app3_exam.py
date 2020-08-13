from flask import Flask, render_template
import datetime
import RPi.GPIO as GPIO

import smbus
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

bus = smbus.SMBus(1)
addr = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe


cmd =""

@app.route("/")
def hello():
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

        #cmd = "echo %resp > /dev/rfcomm0"

        #ipaddr = run_cmd(cmd)
        
        templateData = {
             'title' : 'TEST-2',
             'time': timeString,
             'temp': temp1,
             'msg': resp
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

def run_cmd(cmd):
      p = Popen(cmd, shell=True, stdout=PIPE)
      output = p.communicate()[0]
      return output

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
