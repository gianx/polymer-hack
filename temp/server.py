#!/usr/bin/env python
# -*- coding: utf-8 -*-
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template
import json

class message():
    sender = ''
    msg = ''
    def __init__(self, sender, msg):
        self.sender = sender
        self.msg = msg

class chat():
    
    history = []
    
    def __init__(self):
        pass
    
    def msg(self,msg):
        self.history.append(message('Default sender',msg))
        pass
    
    def __str__(self):
        out = ""
        for x in self.history:
            out += x.sender + " : " + x.msg + "<br>"
        return out

app = Flask(__name__)

@app.route('/')
def index():
    print "ciao"
    return render_template('./index.html')

@app.route('/api')
def api():
    global mychat
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            message = ws.receive()
            mychat.msg(message)
            ws.send(str(mychat))
            #ws.send(message)
    return

if __name__ == '__main__':
    mychat = chat()
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    """
    
    mychat.msg("ciao")
    mychat.msg("a")
    mychat.msg("tutti")
    print str(mychat)
    """
