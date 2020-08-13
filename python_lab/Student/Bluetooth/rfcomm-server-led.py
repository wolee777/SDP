# file: rfcomm-server.py
#
# desc: simple demonstration of a server application that uses RFCOMM sockets
#

from bluetooth import *
import RPi.GPIO as GPIO
import time

# LED configuration
led_1 = 14
led_2 = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_1, GPIO.OUT) 
GPIO.setup(led_2, GPIO.OUT)

# bluetooth configuration
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid =  "00001800-0000-1000-8000-00805F9B34FB"

advertise_service( server_sock, "raspberrypi",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )


def led_toggle():
    for i in range (3):
        GPIO.output(led_1, True) 
        GPIO.output(led_2, True) 
        time.sleep(1)
        GPIO.output(led_1, False)
        GPIO.output(led_2, False)
        time.sleep(1)
        
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        bytedata = client_sock.recv(1024)
        
        data = bytedata.decode()
        
        if data == "exit": break
        print("received [%s]" % data)

        # LED Control part
        if data == "0":
            GPIO.output(led_1, False)
            GPIO.output(led_2, False)
        elif data == "2":
            GPIO.output(led_1, True)
            GPIO.output(led_2, True)
        elif data == "3":
            led_toggle()
            
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
