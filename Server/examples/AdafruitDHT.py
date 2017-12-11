##  @file: AdafruitDHT.py
##  @brief: Implementation of the Temperature/Humidity sensing and QT GUI, along with transmission via MQTT to AWS IOT
##  @Authors: Rhea Cooper, Ashish Tak (University of Colorado, Boulder)
##  @Date: 11/12/2017

##!/usr/bin/python
##References:https://github.com/adafruit/Adafruit_Python_DHT
##           https://www.tutorialspoint.com/pyqt/pyqt_basic_widgets.htm
##           https://www.tutorialspoint.com/python/python_database_access.htm

import sys 
import time 
import Adafruit_DHT 
import datetime 
import PyQt4 
from PyQt4 import QtCore, QtGui,uic 
from A import Ui_MainWindow        
import MySQLdb
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import boto3
from botocore.exceptions import ClientError


#Callback function to echo the data sent to the MQTT client
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


class MyMainWindow(QtGui.QMainWindow):
    """main class that contains all the methods required for the GUI""" 
 
    def __init__(self, parent=None):
        """constructor of class"""
	QtGui.QWidget.__init__(self, parent)
	self.ui = Ui_MainWindow()
	self.ui.setupUi(self)

	"""connecting the push buttons to methods"""
	self.ui.showhum_button.clicked.connect(self.Start)
	self.ui.close_button.clicked.connect(self.close)
	self.ui.avghum_button.clicked.connect(self.ShowAvgHum)
	self.ui.avgtemp_button.clicked.connect(self.ShowAvgTemp)
	self.ui.maxhum_button.clicked.connect(self.ShowMaxHum)
	self.ui.maxtemp_button.clicked.connect(self.ShowMaxTemp)
	self.ui.minhum_button.clicked.connect(self.ShowMinHum)
	self.ui.mintemp_button.clicked.connect(self.ShowMinTemp)
	self.ui.lasthum_button.clicked.connect(self.ShowLastHum)
	self.ui.lasttemp_button.clicked.connect(self.ShowLastTemp)
	self.ui.CtoF_button.clicked.connect(self.Convert)
	self.ui.cb.currentIndexChanged.connect(self.Select)

	"""Setting deafult no. of iterations and Temperature unit"""
        self.ui.iterations = 6
	self.ui.C = 1    

    def Select(self,item):
	"""method to update the number of iterations with the selected value from the combo box"""
        if item == 0:
	   self.ui.iterations=6
	elif item == 1:
	   self.ui.iterations=11
	elif item == 2:
	   self.ui.iterations=16
            
    def Convert(self):
        """method to set change value of Temperature unit conversion variable"""
        if self.ui.C == 0: 
           self.ui.C = 1
        elif self.ui.C == 1:
           self.ui.C = 0

		
    """functions for all the push buttons"""
           
    def ShowMaxHum(self):
	maxhum=max(a)
	showmaxhum="\nMaximum Humidity is " + str(maxhum)[0:6]
	self.ui.display.setText(showmaxhum)
	
    def ShowMinHum(self):
	minhum=min(a)
	showminhum="\nMinimum Humidity is " + str(minhum)[0:6]
	self.ui.display.setText(showminhum)
	
    def ShowMaxTemp(self):
	maxtemp=max(b)
	if self.ui.C==0:
		maxtemp=maxtemp* 9/5.0 + 32
	showmaxtemp="\nMaximum Temperature is " + str(maxtemp)[0:6]
	self.ui.display.setText(showmaxtemp)
		
    def ShowMinTemp(self):
	mintemp=min(b)
        if self.ui.C==0:
                mintemp=mintemp* 9/5.0 + 32
        showmintemp="\nMinimum Temperature is " + str(mintemp)[0:6]
        self.ui.display.setText(showmintemp)
			
    def ShowLastHum(self):
	lasthum=a[-1]
	showlasthum="\nLast value of Humidity is " + str(lasthum)[0:6]
	self.ui.display.setText(showlasthum)
	
    def ShowLastTemp(self):
	lasttemp=b[-1]
        if self.ui.C==0:
                lasttemp=lasttemp* 9/5.0 + 32
        showlasttemp="\nLast value of Temperature is " + str(lasttemp)[0:6]
        self.ui.display.setText(showlasttemp)
        	
    def ShowAvgHum(self):
	avghum=sum(a)/len(a)
	showavghum="\nAverage Humidity is " + str(avghum)[0:6]
	self.ui.display.setText(showavghum)	
		
    def ShowAvgTemp(self):
	avgtemp=sum(b)/len(b)
        if self.ui.C==0:
                avgtemp=avgtemp* 9/5.0 + 32
        showavgtemp="\nAverage Temperature is " + str(avgtemp)[0:6]
        self.ui.display.setText(showavgtemp)
        		
    def Start(self):
        """this method gets the temp, humidity values one by one, displays them along with timestamp and also populates a list that pops up when a predefined number of iterations is done"""
	listWidget=QtGui.QListWidget()
	listWidget.setWindowTitle("List of Values")
	for i in range(1,self.ui.iterations):
            """Read values from the Adafruit sensor for the no. of iterations specified"""
            humidity,temperature = Adafruit_DHT.read_retry(22, 4)
	    if temperature is not None and humidity is not None :
                """Send the Temp (in degree C) and Humidity values to the MQTT client"""
                msg='"Temperature" : "{}", "Humidity" : "{}", "Count" : "{}"'.format(temperature,humidity,i)
                msg='{'+msg+'}'
                myAWSIoTMQTTClient.publish(topic, msg, 1)
                """Convert the temperature for local display if flag for degree F is set"""
                if self.ui.C==1:
                    showtemp="Temperature in degree C is " + str(temperature)
                else:
                    temperature= temperature * 9/5.0 + 32
                    showtemp="Temperature in degree F is " + str(temperature)
                showhum="\nHumidity is : " + str(humidity)
                """Append values to the local list"""
                a.append(humidity)
                b.append(temperature)
                now = datetime.datetime.now()
                showtime="\nCurrent time is : " + now.strftime("%Y-%m-%d %H:%M:%S")
                showtime1=now.strftime("%Y-%m-%d %H:%M:%S")
                c.append(showtime1)
                """Display the Temp, Hum values along with the timestamp on the local QT GUI"""
                self.ui.showhum_window.setText(showtemp + showhum + showtime)
                item=QtGui.QListWidgetItem("Temp: %f , Humidity: %f , Time: %s" % (temperature,humidity,showtime1))
                listWidget.addItem(item)
                if temperature > 35:
                    w=QtGui.QWidget()
                    result=QtGui.QMessageBox.warning(w, "Message", "Temperature too high")
                else:
                    self.ui.statusbar.showMessage("Temperature optimal",1000000)
                """insert the values into the table"""
                sql = "INSERT INTO INFO(TEMPERATURE, HUMIDITY,TIME) VALUES ('%f', '%f', '%s')" % (temperature,humidity,showtime1)
                try:
                    """Execute the SQL command"""
                    cursor.execute(sql)
                    """Commit changes to the database"""
                    db.commit()
                except:
                    """Rollback in case there is any error"""
                    db.rollback()
	    else:
                """handling not receiving data"""
                shownotemp="Sorry, temperature , humidity unavailable . Try again "
                self.ui.showhum_window.setText(shownotemp)
            """Wait for 5 seconds before the next reading"""
            time.sleep(5)
        try:
			response = client.send_email(
				Destination={
					'ToAddresses': [
						RECIPIENT,
					],
				},
				Message={
					'Body': {
						'Html': {
							'Charset': CHARSET,
							'Data': BODY_HTML,
						},
						'Text': {
							'Charset': CHARSET,
							'Data': BODY_TEXT,
						},
					},
					'Subject': {
						'Charset': CHARSET,
						'Data': SUBJECT,
					},
				},
				Source=SENDER,
			)
		# Display an error if something goes wrong.	
        except ClientError as e:
			print(e.response['Error']['Message'])
        else:
			print("Email sent! Message ID:"),
			print(response['ResponseMetadata']['RequestId'])
        listWidget.show()
        listWidget.exec_()



"""local list for humidity, temperature and timestamps respectively"""
a=[]     
b=[]     
c=[]     

#Set up the Host URL and Certifiactes/Keys
host = "a1ah5fy1h4v4k9.iot.us-east-1.amazonaws.com"
rootCAPath = "/home/pi/Desktop/EID_Project3/EID_Project3/Certificates/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
certificatePath = "/home/pi/Desktop/EID_Project3/EID_Project3/Certificates/57ca76974a-certificate.pem.crt"
privateKeyPath = "/home/pi/Desktop/EID_Project3/EID_Project3/Certificates/57ca76974a-private.pem.key"
clientId = 'iotconsole-1510025171163-0'
topic = 'P3'

#Initialize Logger
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
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

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Rhea Cooper <rheabcooper@gmail.com>"

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
RECIPIENT = "rhea.cooper@colorado.edu"

AWS_REGION = "us-east-1"

# The subject line for the email.
SUBJECT = "Amazon SES Test (SDK for Python)"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Values received on server\r\n"
             
            )
            
# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>MQTT msgs sent</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """            

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

    
 
"""connecting to the database"""
db = MySQLdb.connect("localhost","root","root","DB1" )
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS INFO")

"""Create sql table as per requirement"""
sql = """CREATE TABLE INFO (
	 ID INT NOT NULL AUTO_INCREMENT,
         TEMPERATURE  FLOAT NOT NULL,
         HUMIDITY  FLOAT NOT NULL,
         TIME VARCHAR(256) NOT NULL, 
	 PRIMARY KEY (ID))"""
cursor.execute(sql)

"""instantiating the above class"""
app=QtGui.QApplication(sys.argv)
myapp=MyMainWindow()
myapp.show()
sys.exit(app.exec_())
