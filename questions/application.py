from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from questions.flaskrun import flaskrun
import json
import jinja2
import csv
import random
import urllib.request
import codecs
import boto3
from random import shuffle

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

#MS CSV
data = urllib.request.urlopen('https://raw.githubusercontent.com/DannylDasilva/F/master/MS.csv')
reader = csv.reader(codecs.iterdecode(data, 'utf-8', errors='replace'))
build = list(reader)
columns = build[0]
build = build[1:]
MS2 = {}
for row in build:
  dict = {columns[1]: row[1], columns[2]: row[2], columns[3]: row[3]}
  MS2[row[0]] = dict

#ES CSV
data = urllib.request.urlopen('https://raw.githubusercontent.com/DannylDasilva/F/master/ES.csv')
reader = csv.reader(codecs.iterdecode(data, 'utf-8', errors='replace'))
build = list(reader)
columns = build[0]
build = build[1:]
ES2 = {}
for row in build:
  dict = {columns[1]: row[1], columns[2]: row[2], columns[3]: row[3]}
  ES2[row[0]] = dict 


application = Flask(__name__, template_folder='templates')
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)



# simple flask app
@application.route('/simple/admin')
def simple_admin():
  return render_template('simple/admin.html')

@application.route('/simple/client')
def simple_client():
  return render_template('simple/client.html')

@application.route('/simple/feed')
def simple_feed():
  return render_template('simple/feed.html')


# Socket to transmit data to client Simple App
@application.route('/admin/data', methods=['POST'])
def admindata():
    socketio.emit('msg', {'msg': 'data'}, broadcast=True)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# Live app
@application.route('/admin')
def admin():
  return render_template('index.html')

@application.route('/admin/reset', methods=['POST'])
def adminreset():
  global redlevel 
  global bluelevel
  redlevel = ''
  bluelevel = ''
  socketio.emit('msg', {'msg': 'reset'}, broadcast=True)
  return response

redlevel = " "
bluelevel = " "

@application.route('/admin/start', methods=['Post'])
def test4():
  global redlevel 
  global bluelevel
  #hs = render_template('HS.html', row= HS)
  #time.sleep(1)
  redform = request.form.get('Red')
  blueform = request.form.get('blue')
  redlevel = redform
  bluelevel = blueform
  print(redlevel)
  #select1 = request.form.get('Blue')
  socketio.emit('msg', {'q': 'q', 'Red': str(redform), 'delay': int(request.form['delay']), 'total': int(request.form['total'])}, broadcast=True)
  return '<html>working</html>'


@application.route('/screen')
def screen():
  return render_template('screen.html')


@application.route('/team/<color>')
def team_screen(color):
  print(redlevel)
  if color == 'Red':
    level = redlevel 
  else:
    level = bluelevel
  print(level)
  if level == "HS": 
    dictionary = HS2[random.choice(list(HS2.keys()))]
  elif level == "MS": 
    dictionary = MS2[random.choice(list(MS2.keys()))]
  elif level == "ES": 
    dictionary = ES2[random.choice(list(ES2.keys()))]
  else:
     dictionary = {"":""}
  return render_template('team.html', color=color, row=dictionary)


#s3 demo
@application.route('/s3/admin')
def s3_admin():
  return render_template('s3/index.html')

@application.route('/s3/admin/reset', methods=['POST'])
def s3_reset():
  socketio.emit('msg', {'msg': 'reset'}, broadcast=True)

@application.route('/s3/admin/start', methods=['POST'])
def s3_start():
    s3 = boto3.client('s3')
    blue_objects = s3.list_objects_v2(Bucket="robot-drone-league", Prefix=request.form['blue'] + '/')
    blue_questions = []
    for obj in blue_objects['Contents']:
      if obj['Size'] > 0:
        blue_questions.append('{}/{}/{}'.format(s3.meta.endpoint_url, 'robot-drone-league', obj['Key']))

    shuffle(blue_questions)
    red_objects = s3.list_objects_v2(Bucket="robot-drone-league", Prefix=request.form['red'] + '/')
    red_questions = []
    for obj in red_objects['Contents']:
      if obj['Size'] > 0:
        red_questions.append('{}/{}/{}'.format(s3.meta.endpoint_url, 'robot-drone-league', obj['Key']))
    shuffle(red_questions)

    socketio.emit('msg', {'blue': blue_questions, 'red': red_questions, 'delay': int(request.form['delay']), 'total': int(request.form['total'])}, broadcast=True)

    return ""


@application.route('/s3/screen')
def s3_screen():
  return render_template('s3/screen.html')


@application.route('/s3/team/<color>')
def s3_team_screen(color):
  return render_template('s3/team.html', color=color)


# run Flask app in debug mode
if __name__ == '__main__':
    flaskrun(socketio, application)
