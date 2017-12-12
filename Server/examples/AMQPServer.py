##  @file: AMQPServer.py
##  @brief: Implementation of the AMQP Server code to return the data back to the client
##  @Authors: Rhea Cooper, Ashish Tak (University of Colorado, Boulder)
##  @Date: 11/12/2017

import pika, os, time

#Callback function to act on incoming messages
def process_function(msg):
  print(" Received message at AMQP Server %r" % msg)
  url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
  connection = pika.BlockingConnection(params)
  channel = connection.channel()
  channel.queue_declare(queue='data')
  channel.basic_publish(exchange='', routing_key='data', body=msg)
  print ("Message sent back to AMQP client")
  connection.close()
  return;

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='data') # Declare a queue

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  process_function(body)

# set up subscription on the queue
channel.basic_consume(callback,
  queue='data',
  no_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()
