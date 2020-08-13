import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags,rc):
  print ("Connected with result code " + str(rc))
  client.subscribe("hello/world")

def on_message(client, userdata, msg):
  print ("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload))

client = mqtt.Client()        # MQTT Client 
client.on_connect = on_connect     # on_connect callback 
client.on_message = on_message   # on_message callback 

#client.connect("test.mosquitto.org", 1883, 60)   # MQTT 
client.connect("localhost", 1883, 60)   # iCORE-SDP Broker 

client.loop_forever()
