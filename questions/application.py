from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
  return render_template('admin.html')


@app.route('/client')
def client():
  return render_template('client.html')


@app.route('/feed')
def feed():
  return render_template('feed.html')


# Socket to transmit data to client
@app.route('/admin/data', methods=['POST'])
def data():
    socketio.emit('msg', {'msg': 'data'}, broadcast=True)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}



# run Flask app in debug mode
if __name__ == '__main__':
    socketio.run(app, debug=True)