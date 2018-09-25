from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from questions.flaskrun import flaskrun
import json


application = Flask(__name__, template_folder='templates')
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)


@application.route('/')
def index():
  return render_template('admin.html')


@application.route('/client')
def client():
  return render_template('client.html')


@application.route('/feed')
def feed():
  return render_template('feed.html')


# Socket to transmit data to client
@application.route('/admin/data', methods=['POST'])
def data():
    socketio.emit('msg', {'msg': 'data'}, broadcast=True)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}



# run Flask app in debug mode
if __name__ == '__main__':
    flaskrun(socketio, application)