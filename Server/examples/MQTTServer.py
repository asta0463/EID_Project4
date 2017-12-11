##  @file: ServerWS.py
##  @brief: Implementation of Server Side MQTT
##  @Authors: Rhea Cooper, Ashish Tak (Univeristy of Colorado, Boulder)
##  @Date: 12/11/2017


import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("Project4")

def on_publish(client,userdata,result):             #create function for callback
  print("data published \n")
  pass
  

def on_message(client, userdata, msg):
  #print("message received " ,str(msg.payload.decode("utf-8")))
  #print("message topic=",msg.topic)
  #print("message qos=",msg.qos)
  #print("message retain flag=",msg.retain)
  #print("Publishing message to topic")
  client.publish("P4",str(msg.payload.decode("utf-8")))
  

def on_subscribe(client, userdata, mid, granted_qos):
  print("sub ack " + str(mid) + "qos " +str(granted_qos))
    
client = mqtt.Client()
broker_address="iot.eclipse.org"
client.connect(broker_address)

client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.loop_forever()
