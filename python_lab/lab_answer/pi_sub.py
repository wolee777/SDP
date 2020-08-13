# pi_sub.py
import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO
import time

led1 = 14
led2 = 15

GPIO_RP = 4
GPIO_RN = 25
GPIO_EN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buzzer_pin=13
GPIO.setup(buzzer_pin, GPIO.OUT) 

scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]
scale2 = [ 1047, 1175, 1319, 1397, 1568, 1760, 1976, 2093 ]
p = GPIO.PWM(buzzer_pin, 100)
GPIO.output(buzzer_pin, True)

def buzzer_on():

    p.start(100) # start the PWM on 100% duty cycle
    p.ChangeDutyCycle(90) # change the duty cycle to 90%

    for i in range(8):
        p.ChangeFrequency(scale[i])
        time.sleep(0.1)
    p.stop()   # stop the PWM output

def led_init(led1,led2):
        GPIO.setup(led1, GPIO.OUT)
        GPIO.setup(led2, GPIO.OUT)

def led_on(led_pin):
        GPIO.output(led_pin, True)

def led_off(led_pin):
        GPIO.output(led_pin, False)

def motor_init():
        GPIO.setup(GPIO_RP, GPIO.OUT)
        GPIO.setup(GPIO_RN, GPIO.OUT)
        GPIO.setup(GPIO_EN, GPIO.OUT)

def motor_forward():
        print ('motor forward')
        GPIO.output(GPIO_RP, True)
        GPIO.output(GPIO_RN, False)
        GPIO.output(GPIO_EN, True)

def motor_backward():
        print ('motor backward')
        GPIO.output(GPIO_RP, False)
        GPIO.output(GPIO_RN, True)
        GPIO.output(GPIO_EN, True)

def motor_stop():
        print ('motor stop')
        GPIO.output(GPIO_EN, False)

def on_connect(client, userdata, flags,rc):
        print ("Connected with result code " + str(rc))
        client.subscribe("icore-sdp/buzzer")
        client.subscribe("icore-sdp/dc_motor")
        client.subscribe("icore-sdp/led1")
        client.subscribe("icore-sdp/led2")

def motor_message_control(buf_str):
        if buf_str == 'on':
            print('MOTOR: ',buf_str)
            motor_forward()
                
        elif buf_str == 'off':
            print('MOTOR: ',buf_str)
            motor_stop()

def led1_message_control(buf_str):
        if buf_str == 'on':
            print('LED1: ',buf_str)
            led_on(led1)
                
        elif buf_str == 'off':
            print('LED1: ',buf_str)
            led_off(led1)

def led2_message_control(buf_str):
        if buf_str == 'on':
            print('LED2: ',buf_str)
            led_on(led2)
                
        elif buf_str == 'off':
            print('LED2: ',buf_str)
            led_off(led2)

def buzzer_message_control(buf_str):
        if buf_str == 'on':
            print('buzzer: ',buf_str)
            buzzer_on()
    
def on_message(client, userdata, msg):
        buf_str = msg.payload.decode()   # decode() : convert byte to string
        print ('[Topic:', msg.topic + ']  [Message:' + buf_str + ']')

        if msg.topic == 'icore-sdp/led1':
            led1_message_control(buf_str)
            
        elif msg.topic == 'icore-sdp/led2':
            led2_message_control(buf_str)
    
        elif msg.topic == 'icore-sdp/dc_motor':
            motor_message_control(buf_str)

        elif msg.topic == 'icore-sdp/buzzer':
            buzzer_message_control(buf_str)

if __name__ == "__main__":

        led_init(led1,led2)

        motor_init()
        
        client = mqtt.Client()           # MQTT Client
        client.on_connect = on_connect   # on_connect callback
        client.on_message = on_message   # on_message callback
        client.connect("localhost", 1883, 60)   # MQTT
#        client.connect("test.mosquitto.org", 1883, 60)   # MQTT
        client.loop_forever()
