from flask import Flask, render_template, request, jsonify, url_for
import uuid
import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit 
import jinja2
import csv
import random
#import csvs and random select
with open('HS.csv', 'r') as infile:
  reader = csv.reader(infile)
  build = list(reader)
columns = build[0]
build = build[1:]
HS2 = {}
for row in build:
  dict = {columns[1]: row[1], columns[2]: row[2], columns[3]: row[3]}
  HS2[row[0]] = dict
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

# create flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# index route, shows index.html view
@app.route('/')
def index():
  return render_template('index.html')



@app.route('/screen')
def screen():
  return render_template('screen.html')

# feed route, shows feed.html view
@app.route('/red')
def red():
  return render_template('red.html')
  
@app.route('/blue')
def blue():
  return render_template('blue.html',)


@app.route('/HS')
def HS():
  return render_template('HS.html',  row=HS2[random.choice(list(HS2.keys()))])
  

@app.route('/MS')
def MS():
  return render_template('MS.html', row=MS2[random.choice(list(MS2.keys()))])


@app.route('/ES')
def ES():
  return render_template('ES.html', row=ES2[random.choice(list(ES2.keys()))])



@app.route('/end')
def end():
  return render_template('end.html')


@app.route('/files')
def files():
  return render_template('files.html')


#red High School Middle School and Elementary teams sockets, 2 for each is required
@app.route('/admin/redHS', methods=['POST'])
def redHS(): 
  socketio.emit('msg', {'msg': 'redHS'}, broadcast=True)

@app.route('/admin/redMS', methods=['POST'])
def redMS():
  socketio.emit('msg', {'msg': 'redMS'}, broadcast=True)
  

@app.route('/admin/redES', methods=['POST'])
def redES():
  socketio.emit('msg', {'msg': 'redES'}, broadcast=True)
 

@app.route('/admin/blueHS', methods=['POST'])
def blueHS(): 
  socketio.emit('msg', {'msg': 'blueHS'}, broadcast=True)

@app.route('/admin/blueMS', methods=['POST'])
def blueMS():
  socketio.emit('msg', {'msg': 'blueMS'}, broadcast=True)
  

@app.route('/admin/blueES', methods=['POST'])
def blueES():
  socketio.emit('msg', {'msg': 'blueES'}, broadcast=True)
  


#reset Function
@app.route('/admin/reset', methods=['POST'])
def reset():
  socketio.emit('msg', {'msg': 'reset'}, broadcast=True)
  




# run Flask app in debug mode
if __name__ == '__main__':
    socketio.run(app)
