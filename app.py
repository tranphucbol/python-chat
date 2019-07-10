from flask import (
    Flask,
    Response,
    redirect,
    render_template,
    request,
    session,
    jsonify
)

import os
import datetime
from flask_socketio import SocketIO, emit, join_room, leave_room, \
close_room, rooms, disconnect

import models.user as User
import models.channels as Channel


app = Flask(__name__)
socketio = SocketIO(app)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(message):
    emit('my_respone', {'data': message['data']})

# @socketio.on('connect')
# def connectRoom():
#     if 'user' in session:
#         channels = Channel.getAllChannel(session['user'])
#         for channel in channels:
#             join_room(channel['channel_id'])
            # print(rooms())

@socketio.on('join')
def join(message):
    join_room(message['room'])
    print(rooms())
    emit('my_response', {
        'data': 'In rooms: ' + ', '.join(rooms())
    })

@socketio.on('leave')
def leave(message):
    leave_room(message['room'])
    emit('my_response',{
        'data': 'In rooms: ' + ', '.join(rooms())
    })

@socketio.on('close_room')
def close(message):
    emit('my_response', {
        'data': 'Room ' + message['room'] + ' is closing',
    }, room=message['room'])
    close_room(message['room'])

@socketio.on('my_room_event')
def send_room_message(message):
    print(message)
    emit('my_response',{
        'data': message['data'],
        'room': message['room'],
        'id': message['id']       
    }, room=message['room'])

# @socketio.on('disconnect_request')
# def disconnect_request():

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'user' in session:
            return redirect('/')
        else:
            if User.checkUser(request.form['username'], request.form['password']):
                session['user'] = request.form['username']
            else: return redirect('/login')
    return render_template('login.html')

@app.route("/friends", methods=['GET', 'POST'])
def getFriends():
    if request.method == 'GET':
        if 'user' in session:
            channels = Channel.getAllChannel(session['user'])
            print(channels)
            return jsonify(channels)
        else:
            return jsonify({
                'error': 'you must login'
            })

@app.route("/")
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', user=session['user'])

if (__name__ == "__main__"):
    app.secret_key = os.urandom(24)
    socketio.run(app, debug=True)