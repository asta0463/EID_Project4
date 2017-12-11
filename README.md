Protocol Comparison
==================================
Repository for the fourth Project of ECEN 5053-002 : Embedded Interface Design   
This project involves comparison of the efficiency of 3 IOT Protocols (MQTT,COAP,WEBSOCKETS) based on the roundtrip time taken to transfer a message from Client to Server and back to the Client.


Authors: Rhea Cooper and Ashish Tak

Date: 12/10/2017

Installation Instructions:
--------------------------------
1.Install all the python libraries and dependencies :
``````````````````````````````````````````````````````````` 
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl
sudo python setup.py install
`````````````````````````````````````````````````````````````             
2.Install QT4 designer on the Server and Client Pi:
```````````````````````````````````````````````````````````
sudo apt-get install qt4-designer
```````````````````````````````````````````````````````````
3.Install PyQt4 on the Server and Client Pi: 
```````````````````````````````````````````````````````````
sudo apt-get install pyqt4
```````````````````````````````````````````````````````````
5.Install the following on the Pis for COAP:
```````````````````````````````````````````````````````````
sudo pip install twisted==13.1.0
sudo pip install txthings
```````````````````````````````````````````````````````````
6.Install the following on the Pis for WebSockets:
```````````````````````````````````````````````````````````
sudo pip install tornado
sudo pip install websocket-client
```````````````````````````````````````````````````````````
7.Install the following on the Pis for WebSockets:
```````````````````````````````````````````````````````````
sudo pip install paho-mqtt
```````````````````````````````````````````````````````````
8.Install boto3 on the Client Pi: 
```````````````````````````````````````````````````````````
pip install boto3
```````````````````````````````````````````````````````````
9.To use Boto 3, you must first import it and tell it what service you are going to use:
```````````````````````````````````````````````````````````
import boto3
sqs = boto3.resource('sqs')
```````````````````````````````````````````````````````````
10.Install numpy for graph on the Client Pi:
```````````````````````````````````````````````````````````
sudo pip install numpy
```````````````````````````````````````````````````````````
11.In the "Client" folder of the Client Pi run the following :
```````````````````````````````````````````````````````````
python Client.py
```````````````````````````````````````````````````````````
12.Press the REQUEST DATA button.
13.In the of the "examples" folder of "Server" folder of the Server Pi run the following one by one and subsequently press the required button on the Client Side GUI:
```````````````````````````````````````````````````````````
python MQTTServer.py
python WSServer.py
python COAPClient.py
```````````````````````````````````````````````````````````
14.Press the COMPARE button on the QT GUI of Client Pi to view the graphs.


Project Work
---------------------------------
This project is an extension of Project3. The message with the 30(or less) values from the SQS queue is used for the Protocol Comparison. The message is passed to an MQTT Server from the Client Pi and back from the Server to the Client. The roundtrip time is calculated. 
The same is repeated for WebSockets and COAP. 
Our Results:
WebSockets is the fastest followed by MQTT and then COAP.


 

References
-------------------------------------------------
1.https://github.com/adafruit/Adafruit_Python_DHT.git

2.https://www.tutorialspoint.com/pyqt/pyqt_basic_widgets.htm

3.https://pythonspot.com/en/pyqt4-gui-tutorial/

4.https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview

5.https://github.com/aws/aws-iot-device-sdk-python

6.http://boto3.readthedocs.io/en/latest/guide/sqs.html

7.https://pythonspot.com/en/matplotlib-bar-chart/

8.http://www.steves-internet-guide.com/into-mqtt-python-client/

9.http://www.giantflyingsaucer.com/blog/?p=4602

10.https://github.com/mwasilak/txThings





10
