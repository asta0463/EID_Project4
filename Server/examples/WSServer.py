##  @file: ServerWS.py
##  @brief: Implementation of Server Side Web Socket Handler
##  @Authors: Rhea Cooper, Ashish Tak (Univeristy of Colorado, Boulder)
##  @Date: 12/09/2017

#!/usr/bin/python


import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import socket
  
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("opened")
  
    def on_message(self, message):
        print("Your message is received: ")
        #sending received msg back to client
        self.write_message(message) 
  
    def on_close(self):
        print("closed")
  
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/websocket', WebSocketHandler)
        ]
 
        tornado.web.Application.__init__(self, handlers)
  

if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    myIP= socket.gethostbyname(socket.gethostname())
    print('WS Server started at %s' %myIP)
    tornado.ioloop.IOLoop.instance().start()

