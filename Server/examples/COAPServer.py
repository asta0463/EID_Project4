##  @file: ServerWS.py
##  @brief: Implementation of Server Side COAP
##  @Authors: Rhea Cooper, Ashish Tak (Univeristy of Colorado, Boulder)
##  @Date: 10/23/2017

import sys
from twisted.internet import defer
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.python import log
import txthings.resource as resource
import txthings.coap as coap

class CounterResource (resource.CoAPResource):
    """
    Example Resource which supports only GET method. Response is a
    simple counter value.
    """

    def __init__(self, start=0):
        resource.CoAPResource.__init__(self)
        self.counter = start
        self.visible = True
        self.addParam(resource.LinkParam("title", "Counter resource"))

    def render_GET(self, request):
        response = coap.Message(code=coap.CONTENT, payload=request.payload)
        return defer.succeed(response)


# Resource tree creation
#log.startLogging(sys.stdout)
root = resource.CoAPResource()
counter = CounterResource(5000)
root.putChild('counter', counter)

endpoint = resource.Endpoint(root)
reactor.listenUDP(coap.COAP_PORT, coap.Coap(endpoint)) 
reactor.run()
