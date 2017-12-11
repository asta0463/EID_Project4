##  @file: Client.py
##  @brief: Implementation of the Client side GUI, and reception of data from the SQS queue
##  @Authors: Rhea Cooper, Ashish Tak (University of Colorado, Boulder)
##  @Date: 11/12/2017

#!/usr/bin/python
#References: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-tutorials.html and https://boto3.readthedocs.io/en/latest/index.html

import sys 
import time 
import datetime
import thread
import PyQt4 
from PyQt4 import QtCore, QtGui,uic 
from P3 import Ui_MainWindow        

#Importing modules for IOT client
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import boto3
from boto3.session import Session
import logging
import paho.mqtt.client as mqtt

import websocket
import numpy as np

#importing required modules to plot graph
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

#importing modules required for CoAp
from twisted.internet.defer import Deferred
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.python import log
import txthings.coap as coap
import txthings.resource as resource
from ipaddress import ip_address

#Lists to maintain the values fetched from the SQS queue
AvgT=[]     
MaxT=[]     
MinT=[]
LatestT=[]
AvgH=[]
MaxH=[]
MinH=[]
LatestH=[]
total=[]

#globals
body=0
t1_mqtt=0
t2_mqtt=0
t3_mqtt=0
t1_web=0
t2_web=0
t3_web=0
t1_coap=0
t2_coap=0
t3_coap=0

#next 3 functions are for MQTT
def on_message(client, userdata, message):
	global t2_mqtt
	global t3_mqtt
	t2_mqtt=time.time()
	print("%f" % t2_mqtt)
	print("%f" % t1_mqtt)
	t3_mqtt=t2_mqtt-t1_mqtt
	print(" Time difference for MQTT is %f" % t3_mqtt)
	

def on_subscribe(client, userdata, mid, granted_qos):
	print("sub ack " + str(mid) + "qos " +str(granted_qos))
	

def on_publish(client,userdata,result): #create function for callback
        print("data published \n")
        pass


class MyMainWindow(QtGui.QMainWindow):
    """main class that contains all the methods required for the Client side GUI""" 
 
    def __init__(self, parent=None):
        """constructor of class"""
	QtGui.QWidget.__init__(self, parent)
	self.ui = Ui_MainWindow()
	self.ui.setupUi(self)
	
	"""connecting the push buttons to methods"""
	self.ui.request_button.clicked.connect(self.Start)  
	self.ui.Humgraph_button.clicked.connect(self.HumGraph)
	self.ui.Tempgraph_button.clicked.connect(self.TempGraph)
	self.ui.CtoF_button.clicked.connect(self.Convert)
	self.ui.figure=plt.figure(figsize=(15,5))
	self.ui.canvas=FigureCanvas(self.ui.figure)
	self.ui.gridLayout.addWidget(self.ui.canvas,1,0,1,2)
	self.ui.MQTT_button.clicked.connect(self.MQTTTest)
        self.ui.websockets_button.clicked.connect(self.WebTest)
        self.ui.COAP_button.clicked.connect(self.COAPTest)
        #self.ui.AMQP_button.clicked.connect(self.AMQPTest)
        self.ui.compare_button.clicked.connect(self.Compare)

        """Set the default value for Temperature Unit"""
	self.ui.C = 1

    def MQTTTest(self):
        client.loop_start() #start the loop
        #print(total)
        global t1_mqtt
        t1_mqtt=time.time();
        #print("body of msg is : %s" % format(total))
        print("Publishing message to topic")
        client.publish("Project4",format(total))
        print("Subscribing to topic","Project4/Message/Return")
        client.subscribe("P4")
        time.sleep(1) # wait
        client.loop_stop() #stop the loop

    def WebTest(self):
        #websocket.enableTrace(True)
        #ws = create_connection("ws://echo.websocket.org/")
        ws = websocket.create_connection("ws://10.201.10.43:8080/websocket")
        global t1_web
        t1_web=time.time()
        ws.send("Message is" + format(total))
        print("Sent")
        print("Receiving...")
        result = ws.recv()
        global t2_web
	global t3_web
	t2_web=time.time()
	print("%f" % t2_web)
	print("%f" % t1_web)
	t3_web=t2_web-t1_web
	print("Time taken for WebSockets in seconds is %f" % t3_web)
        print("Received {}".format(result))
        ws.close()

    def COAPTest(self):
        coapclient.requestResource();

    def Compare(self):
        strn="Number of messages:30"
        strm="MQTT : "
        strw="WebSockets :"
        strc="COAP :"
        #stra="AMQP :"
        self.ui.text_window.setText(strn + '\n' + strm + str(t3_mqtt) +'\n' + strw + str(t3_web) +'\n' + strc + str(t3_coap))
        list_all=[]
        list_all.append(t3_mqtt)
        list_all.append(t3_web)
        list_all.append(t3_coap)
        #list_all.append(t3_amqp)
        list_names=[]
        list_names.append("mqtt")
        list_names.append("web")
        list_names.append("coap")
        #list_names.append("amqp")
        objects = ('MQTT', 'Websockets', 'COAP')
        #objects = ('MQTT', 'Websockets', 'COAP', 'AMQP')
        y_pos = np.arange(len(objects))
        performance = list_all
 
        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Seconds')
        plt.title('Protocol Comparison')
        plt.show()
        
    def TempGraph(self):
        """graph plotting Referenced from a youtube video :https://www.youtube.com/watch?v=Wk7CECwebMc"""
 	plt.cla()
	ax=self.ui.figure.add_subplot(111)
	x1=[i for i in range(len(AvgT))]  #value count on x axis
	x2=[i for i in range(len(MaxT))]
	x3=[i for i in range(len(MinT))]
	x4=[i for i in range(len(LatestT))]
	y1=AvgT     #temperature list values on y axis
	y2=MaxT
        y3=MinT
        y4=LatestT
	ax.plot(x1,y1,'b.-')
	ax.plot(x2,y2,'r.-')
	ax.plot(x3,y3,'y.-')
	ax.plot(x4,y4,'g.-')
	ax.set_title('Temperature')
	self.ui.canvas.draw()

    def HumGraph(self):
        """graph plotting Referenced from a youtube video :https://www.youtube.com/watch?v=Wk7CECwebMc"""
        plt.cla()
        ax=self.ui.figure.add_subplot(111)
        x1=[i for i in range(len(AvgH))]  #value count on x axis
	x2=[i for i in range(len(MaxH))]
	x3=[i for i in range(len(MinH))]
	x4=[i for i in range(len(LatestH))]
        y1=AvgH     #humidity list values on y axis
	y2=MaxH
        y3=MinH
        y4=LatestH
	ax.plot(x1,y1,'b.-')
	ax.plot(x2,y2,'r.-')
	ax.plot(x3,y3,'y.-')
	ax.plot(x4,y4,'g.-')				
        ax.set_title('Humidity')
        self.ui.canvas.draw()

    def Convert(self):
        """method to set change value of Temperature unit conversion variable"""
        if self.ui.C == 0: 
           self.ui.C = 1
        elif self.ui.C == 1:
           self.ui.C = 0
    	
    def Start(self):
        """this method gets the messages from the SQS queue and populates a list that pops up"""
	listWidget=QtGui.QListWidget()
	listWidget.setWindowTitle("List of Values")
	
        #Set up the Host URL and Certificates/Keys
        host = "a1ah5fy1h4v4k9.iot.us-east-1.amazonaws.com"
        rootCAPath = "/home/pi/Desktop/EID_Project3/EID_Project3/Certificates/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
        certificatePath = "/home/pi/Desktop/EID_Project3/EID_Project3/Certificates/57ca76974a-certificate.pem.crt"
        privateKeyPath = "/home/pi/Desktop/EID_Project3/EID_Project3/Certificates/57ca76974a-private.pem.key"
        clientId = 'iotconsole-1510025171163-0'
        topic = 'P3'

        # Configure logging
        logger = logging.getLogger("AWSIoTPythonSDK.core")
        logger.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

        # Initialize AWSIoTMQTTClient
        myAWSIoTMQTTClient = None
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host,8883)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Create the Boto3 Session
        session = Session(
            aws_access_key_id='AKIAIBMHYZLYB4EEOWUQ',
            aws_secret_access_key='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',
            region_name='us-east-1',
        )
        client = session.client('sqs')

        # Get the Queue URL
        response = client.get_queue_url(
            QueueName='P3_2'
        )
        url = response['QueueUrl']

        #Initialize the count and the Temp, Hum lists
        count=0
        AvgT[:]=[]     
        MaxT[:]=[]     
        MinT[:]=[]
        LatestT[:]=[]
        AvgH[:]=[]
        MaxH[:]=[]
        MinH[:]=[]
        LatestH[:]=[]
        #Fetch the messages one by one 
        while count<30:
            messages = client.receive_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/499557241041/P3_2',
                AttributeNames=['All'],
                MaxNumberOfMessages=1,
                VisibilityTimeout=60,
                WaitTimeSeconds=5
                )
            try:
                m = messages['Messages'][0]
                global body
                body= m['Body']
                count=count+1   #Increment the count if successful in fetching the message body
                att= m['Attributes']
                timestamp=datetime.datetime.fromtimestamp(float(att['SentTimestamp'])/1000).strftime('%Y-%m-%d %H:%M:%S')
                #Fetch the timestamp for the first and last fetched message respectively
                if count==1:
                    start='Start Timestamp: '+timestamp
                elif count==30:
                    end='End Timestamp: '+timestamp
                    self.ui.text_window.setText(start+'\n'+end)
                #Load the message body in JSON format for parsing 
                d=json.loads(body)
                #Convert to degree F if the flag is cleared
                if self.ui.C==0:
                    Avg = float(d['AvgT']) * 9/5.0 + 32
                    Min = float(d['MinT']) * 9/5.0 + 32
                    Max = float(d['MaxT']) * 9/5.0 + 32
                    Latest = float(d['LatestT']) * 9/5.0 + 32
                else:
                    Avg = float(d['AvgT'])
                    Min = float(d['MinT'])
                    Max = float(d['MaxT'])
                    Latest = float(d['LatestT'])
                #Append each parsed value in the message body into the appropriate lists
                AvgT.append(Avg)
                MinT.append(Min)
                MaxT.append(Max)
                LatestT.append(Latest)
                AvgH.append(d['AvgH'])
                MinH.append(d['MinH'])
                MaxH.append(d['MaxH'])
                LatestH.append(d['LatestH'])
                total.append(AvgT+AvgH+MaxT+MinT+MaxH+MinH+LatestH+LatestT)
                #Display the list on the Client Side widget
                item=QtGui.QListWidgetItem("AvgT: %f , MinT: %f , MaxT: %f , LatestT: %f , AvgH: %f , MinH: %f , MaxH: %f , LatestH: %f, Timestamp: %s" % (Avg, Min, Max, Latest, d['AvgH'], d['MinH'], d['MaxH'], d['LatestH'], timestamp))
                listWidget.addItem(item)
            except KeyError :
                #This exception is caught if there is an error in fetching any of the values from the SQS message, or if there's an error in fetching the message body itself
                if count==0:
                    self.ui.text_window.setText('Sorry, no messages in the SQS queue')
                else:
                    #Display the end timestamp and indicate how many values were successfully fetched from the queue (since <30 in this case)
                    end='End Timestamp: '+timestamp
                    self.ui.text_window.setText(start+'\n'+end+ '\nOnly '+str(count)+' values in the SQS queue')
                break

	listWidget.show()
	listWidget.exec_()

class Agent():
    """
    Class for COAP implementation which performs single GET request to coap.me
    port 5683 (official IANA assigned CoAP port)

    Deferred 'd' is fired internally by protocol, when complete response is received.

    Method printResponse is added as a callback to the deferred 'd'.
    """

    def __init__(self, protocol):
        self.protocol = protocol
        #reactor.callLater(1, self.requestResource)

    def requestResource(self):
        payload= format(total)
        request = coap.Message(code=coap.GET,payload=payload)
        #Send request to "coap://coap.me:5683/test"
        request.opt.uri_path = ('counter',)
        request.opt.observe = 0
        request.remote = (ip_address("10.201.10.43"), coap.COAP_PORT)
        d = protocol.request(request, observeCallback=self.printLaterResponse)
        global t1_coap
        t1_coap=time.time()
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)

    def printResponse(self, response):
        #print 'Result: ' + response.payload
        global t2_coap
	global t3_coap
	t2_coap=time.time()
	print("%f" % t2_coap)
	print("%f" % t1_coap)
	t3_coap=t2_coap-t1_coap
	print("Time taken for COAP in seconds is %f" % t3_coap)
        reactor.stop()

    def printLaterResponse(self, response):
        print 'Observe result: ' + response.payload

    def noResponse(self, failure):
        print 'Failed to fetch resource:'
        print failure
        reactor.stop()


broker_address="iot.eclipse.org"
print("creating  instance")
client = mqtt.Client() #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
#print("Subscribing to topic","Project4/Message")
#client.subscribe("Project4/Message/Return")
client.on_subscribe=on_subscribe
client.on_publish=on_publish

#log.startLogging(sys.stdout)
endpoint = resource.Endpoint(None)
protocol = coap.Coap(endpoint)
coapclient = Agent(protocol)
reactor.listenUDP(61616, protocol)
thread.start_new_thread(reactor.run,((),))
#reactor.run()

#instantiating the above class
app=QtGui.QApplication(sys.argv)
myapp=MyMainWindow()
myapp.show()
sys.exit(app.exec_())
