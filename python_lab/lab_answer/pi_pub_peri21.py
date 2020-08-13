#pi_pub.py
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import smbus2 as smbus
#import smbus
import time


# FOR I2C TEMP & HUMIDITY
bus = smbus.SMBus(1)
th_addr = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe
temp = 0.0
humi = 0.0
th_val = 0
th_data = [0, 0]

# FOR I2C LIGHT SENSOR
light_addr = 0x23
reset = 0x07
con_hr_mode = 0x10

light_data1 = 0
light_data2 = 0
light_val = 0

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

trig = 0
echo = 1
pir  = 24

def get_ultrasonic_distance():
    GPIO.output(trig, False)
    time.sleep(0.1)
 
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
 
    while GPIO.input(echo) == False :  # Peri v 2.1
    #while GPIO.input(echo) == True :  # Peri v 2.0
      pulse_start = time.time()
 
    while GPIO.input(echo) == True :   # Peri v 2.1
    #while GPIO.input(echo) == False : # Peri v 2.0
      pulse_end = time.time()
 
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
 
    #print ("Distance : ", distance, "cm")

    return distance

def get_pir_state():
    return GPIO.input(pir)

def get_temp_value():
        # temperature
        bus.write_byte(th_addr, cmd_temp)
        time.sleep(0.260)

        for i in range(0,2,1):
            th_data[i] = bus.read_byte(th_addr)

        th_val = th_data[0] << 8 | th_data[1]
        temp = -46.85+175.72/65536*th_val
        return temp
    
def get_humi_value():    
	# humidity
	bus.write_byte(th_addr, cmd_humi)
	time.sleep(0.260)
	
	for i in range(0,2,1):
            th_data[i] = bus.read_byte(th_addr)

	th_val = th_data[0] << 8 | th_data[1]
	humi = -6.0+125.0/65536*th_val
	return humi

def get_light_value():
        #light
    	bus.write_byte(light_addr, con_hr_mode)
    	time.sleep(0.2)
    	light_data1 = bus.read_byte(light_addr)
    	light_data2 = bus.read_byte(light_addr)
    	light_val = (light_data1 << 8) | light_data2
    	light_val = light_val / 1.2
    	return light_val

def init_mqtt() :
        mqttc = mqtt.Client("raspi_pub")             # MQTT Client
        mqttc.connect("test.mosquitto.org", 1883)    # MQTT
        return mqttc

    
def main():

    mqttc = init_mqtt()

    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)                # Peri v 2.1
    #GPIO.setup(echo, GPIO.IN,GPIO.PUD_UP)   # Peri v 2.0

    GPIO.setup(pir, GPIO.IN) 

    cnt = 0

    while True :

        val1 = get_temp_value()
        val2 = get_humi_value()

        th_message = 'T:' + format(val1,'.2f') + ' H:' + format(val2, '.2f')
        print(th_message)

        mqttc.publish("icore-sdp/temp_humi", th_message)  # 'temp & humidity' message publishing

        val3 = get_light_value()
        light_message = format(val3,'.2f')
        print('Light: ', light_message)

        mqttc.publish("icore-sdp/light", light_message)   # 'light' message publishing

        distance = get_ultrasonic_distance()
        dist_message = format(distance,'.2f') + ' cm'
        print ('Distance:',dist_message)
     
        mqttc.publish("icore-sdp/ultrasonic", dist_message)   # 'ultra-sonic' message publishing

        state = get_pir_state()
    
        if (state == True) :
            cnt +=1
            pir_message = format(cnt,'d')
            print ('[PIR Count] =', pir_message)
            mqttc.publish("icore-sdp/pir", pir_message)   # 'pir' message publishing
        
        #time.sleep(1)

if __name__ == '__main__':
    main()
  
