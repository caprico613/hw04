import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import time

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your ip
host = "localhost"
topic = "Mbed"

num = 0
tilted = [0 for i in range(0, int(40))]

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    global num
    global tilted
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload))
    tilted[num] = int(msg.payload)
    print(num, tilted[num])
    if num == 39:
        mqttc.disconnect()
        print("disconnect")
        print(tilted)
        t = np.arange(0, 20, 0.5) # time vector;
        print(t)
        plt.plot(t, tilted, 'b', label = 'Tilted')
        plt.legend(loc = 'best')
        plt.xlabel('Time stamp')
        plt.ylabel('Tilted')
        plt.show()
    num = num + 1



def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)


# Loop forever, receiving messages
mqttc.loop_forever()