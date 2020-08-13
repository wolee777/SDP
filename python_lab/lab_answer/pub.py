import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")      # MQTT Client 
#mqttc.connect("test.mosquitto.org", 1883)    # MQTT 
mqttc.connect("localhost", 1883)    # iCORE-SDP Broker 
mqttc.publish("hello/world", "I am Raspberry!! Hello World!")  # 'hello/world'  "Hello World!"
mqttc.loop(2)        # timeout = 2
