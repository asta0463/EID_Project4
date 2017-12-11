##  @file: ServerWS.py
##  @brief: Implementation of Server Side Web Socket Handler
##  @Authors: Rhea Cooper, Ashish Tak (Univeristy of Colorado, Boulder)
##  @Date: 12/09/2017

#!/usr/bin/python
#Reference: http://www.giantflyingsaucer.com/blog/?p=4602

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import socket
  
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("open")
  
    def on_message(self, message):
        print("Your message is received: ")
        self.write_message(message) #sending received msg back to client
  
    def on_close(self):
        print("close")
  
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

