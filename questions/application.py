from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from questions.flaskrun import flaskrun
import json
import jinja2
import csv
import random
import urllib.request
import codecs

#import csvs and random select
#import csvs and random select
data = urllib.request.urlopen('https://raw.githubusercontent.com/DannylDasilva/F/master/HS.csv')
reader = csv.reader(codecs.iterdecode(data, 'utf-8', errors='replace'))
build = list(reader)
columns = build[0]
build = build[1:]
HS2 = {}
for row in build:
  dict = {columns[1]: row[1], columns[2]: row[2], columns[3]: row[3]}
  HS2[row[0]] = dict
'''
#MS CSV
with open('MS.csv', 'r') as infile:
  reader = csv.reader(infile)
  build = list(reader)
columns = build[0]
build = build[1:]
MS2 = {}
for row in build:
  dict = {columns[1]: row[1], columns[2]: row[2], columns[3]: row[3]}
  MS2[row[0]] = dict

#ES CSV
with open('ES.csv', 'r') as infile:
  reader = csv.reader(infile)
  build = list(reader)
columns = build[0]
build = build[1:]
ES2 = {}
for row in build:
  dict = {columns[1]: row[1], columns[2]: row[2], columns[3]: row[3]}
  ES2[row[0]] = dict 
'''

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

# index route, shows index.html view
@application.route('/index')
def admin():
  return render_template('index.html')



@application.route('/screen')
def screen():
  return render_template('screen.html')

# feed route, shows feed.html view
@application.route('/red')
def red():
  return render_template('red.html')
  
@application.route('/blue')
def blue():
  return render_template('blue.html',)


@application.route('/HS')
def HS():
  return render_template('HS.html',  row=HS2[random.choice(list(HS2.keys()))])

''' 
@application.route('/MS')
def MS():
  return render_template('MS.html', row=MS2[random.choice(list(MS2.keys()))])


@application.route('/ES')
def ES():
  return render_template('ES.html', row=ES2[random.choice(list(ES2.keys()))])
'''


@application.route('/end')
def end():
  return render_template('end.html')


@application.route('/files')
def files():
  return render_template('files.html')


#red High School Middle School and Elementary teams sockets, 2 for each is required
@application.route('/admin/redHS', methods=['POST'])
def redHS(): 
  socketio.emit('msg', {'msg': 'redHS'}, broadcast=True)

@application.route('/admin/redMS', methods=['POST'])
def redMS():
  socketio.emit('msg', {'msg': 'redMS'}, broadcast=True)
  

@application.route('/admin/redES', methods=['POST'])
def redES():
  socketio.emit('msg', {'msg': 'redES'}, broadcast=True)
 

@application.route('/admin/blueHS', methods=['POST'])
def blueHS(): 
  socketio.emit('msg', {'msg': 'blueHS'}, broadcast=True)

@application.route('/admin/blueMS', methods=['POST'])
def blueMS():
  socketio.emit('msg', {'msg': 'blueMS'}, broadcast=True)
  

@application.route('/admin/blueES', methods=['POST'])
def blueES():
  socketio.emit('msg', {'msg': 'blueES'}, broadcast=True)
  


#reset Function
@application.route('/admin/reset', methods=['POST'])
def reset():
  socketio.emit('msg', {'msg': 'reset'}, broadcast=True)
  



# run Flask app in debug mode
if __name__ == '__main__':
    flaskrun(socketio, application)
