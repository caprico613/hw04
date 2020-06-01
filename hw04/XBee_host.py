import matplotlib.pyplot as plt
import numpy as np
import serial
import time
import paho.mqtt.client as paho
mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe


num = [0 for i in range(0, int(20))]
t = np.arange(0, 20, 1) # time vector;
store1 = [0 for i in range(0, int(3))]
store2 = [0 for i in range(0, int(3))]
threshold = 0.7071

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)


# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x151\r\n".encode())
char = s.read(3)
print("Set MY 0x151.")
print(char.decode())

s.write("ATDL 0x251\r\n".encode())
char = s.read(3)
print("Set DL 0x251.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")

s.write("/ACC/run 1\r".encode())
line = s.readline() # Read an echo string from K66F terminated with '\n'
print(0, line)
line = s.readline() # Read an echo string from K66F terminated with '\n'
print(line) 
line = s.readline() # Read an echo string from K66F terminated with '\n'
print(line) 
line = s.readline() # Read an echo string from K66F terminated with '\n'
print(line) 
line = s.readline() # Read an echo string from K66F terminated with '\n'
print(line) 
line = s.readline() # Read an echo string from K66F terminated with '\n'
print(line)  
line = s.readline() # Read an echo string from K66F terminated with '\n'
print(line) 

time.sleep(1)

i = 0
while i < 20:
    # send RPC to remote
    s.write("/ACC/run 1\r".encode())
    line = s.readline() # Read an echo string from K66F terminated with '\n'
    print(i, line)
    num[i] = int(line)

    line = s.readline() # Read an echo string from K66F terminated with '\n'
    store1[0] = float(line)
    print(store1[0]) 
    line = s.readline() # Read an echo string from K66F terminated with '\n'
    store1[1] = float(line)
    print(store1[1]) 
    line = s.readline() # Read an echo string from K66F terminated with '\n'
    store1[2] = float(line)
    print(store1[2]) 
    if (store1[2] < threshold and (store1[0] > threshold or store1[0] < -threshold or store1[1] > threshold or store1[1] < -threshold)):
        mesg = "Tilted"
        mqttc.publish(topic, 1) 
        print(mesg)
    else:
        mesg = "Not Tilted"
        mqttc.publish(topic, 0) 
        print(mesg)        

    line = s.readline() # Read an echo string from K66F terminated with '\n'
    store2[0] = float(line)
    print(store2[0]) 
    line = s.readline() # Read an echo string from K66F terminated with '\n'
    store2[1] = float(line)
    print(store2[1])  
    line = s.readline() # Read an echo string from K66F terminated with '\n'
    store2[2] = float(line)
    print(store2[2]) 
    if (store2[2] < threshold and (store2[0] > threshold or store2[0] < -threshold or store2[1] > threshold or store2[1] < -threshold)):
        mesg = "Tilted"
        mqttc.publish(topic, 1) 
        print(mesg)
    else:
        mesg = "Not Tilted"
        mqttc.publish(topic, 0) 
        print(mesg)  

    i = i + 1

    time.sleep(1)


plt.plot(t, num, 'b', label = 'collect data')
plt.legend(loc = 'best')
plt.xlabel('Time stamp')
plt.ylabel('number')

plt.show()
s.close()

