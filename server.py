#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
import json
import uuid
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

userid = []

def getId():
    global userid
    temp = random.randint(0,10000)
    while temp in userid:
        temp = random.randint(0,10000)
    userid.append(temp)
    return "User"+str(temp)

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    print path
    return app.send_static_file(path)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/old')
def old():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    #output = "<span class='chatuser'>%s</span><span class='chatmessage'>%s</span>"%(str(session['uid']),message['data'])
    emit('my response', {'user': str(session['uid']),'message': message }, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    session['uid'] = getId()
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",port=8000)
