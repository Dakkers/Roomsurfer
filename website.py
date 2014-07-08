#!/usr/bin/python
import ast, json
from collections import OrderedDict
from pymongo import MongoClient
from flask import Flask, render_template, request
app = Flask(__name__)
client = MongoClient()
db = client.roomsurfer
fts = db.freetimes_sorted
fr = db.freerooms


@app.route('/')
def home():
    return render_template('index.html');

@app.route('/projects')
def projects():
    return render_template('projects.html');

@app.route('/roomsurfer', methods=['GET', 'POST'])
def foo():
    if request.method == 'GET':
        return render_template('roomsurfer.html');
        
    else:
        data = ast.literal_eval(request.form.to_dict().keys()[0]) #fucking incredible
        print data 

        #handling room requests
        if data['type'] == 'ROOM':
            return json.dumps(fts.find_one({'room': data['room']})['info'])

        #handling time request
        elif data['type'] == 'TIME':
            roomsList = fr.find_one({'time': data['time']})['info']
            rooms = OrderedDict()
            for room in roomsList:

                building, num = [j.encode('ascii', 'ignore') for j in room.split(' ')]

                if building in rooms:
                    rooms[building].append(num)
                else:
                    rooms[building] = [num]

            return json.dumps(rooms)


        #handling 
        elif data['type'] == 'BUILDING':
            codes = {}

            for SET in fts.find():
                building, num = [j.encode('ascii', 'ignore') for j in SET['room'].split(' ')]

                if building in codes:
                    codes[building].append(num)
                else:
                    codes[building] = [num]

            return json.dumps(codes)


@app.route('/roomsurferKO', methods=['GET', 'POST'])
def foobar():
    if request.method == 'GET':
        return render_template('roomsurferKO.html');
        
    else:
        data = request.form.to_dict()

        #handling room requests
        if data['type'] == 'ROOM':
            return json.dumps(fts.find_one({'room': data['room']})['info'])

        #handling time request
        elif data['type'] == 'TIME':
            roomsList = fr.find_one({'time': data['time']})
            rooms = OrderedDict()
            if roomsList is not None:
                roomsList = roomsList['info']
                for room in roomsList:

                    building, num = [j.encode('ascii', 'ignore') for j in room.split(' ')]

                    if building in rooms:
                        rooms[building].append(num)
                    else:
                        rooms[building] = [num]
            
            return json.dumps(rooms)


        #handling room request
        elif data['type'] == 'BUILDING':
            codes = {}

            for SET in fts.find():
                building, num = [j.encode('ascii', 'ignore') for j in SET['room'].split(' ')]

                if building in codes:
                    codes[building].append(num)
                else:
                    codes[building] = [num]

            return json.dumps(codes)


@app.route('/1141times.json')
def roomsurfer_times():
    return app.send_static_file('1141times.json');

@app.route('/collatz', methods=['GET', 'POST'])
def collatz():
    if request.method == 'GET':
        return render_template('collatz.html');

@app.route('/lorenz')
def lorenz():
    return render_template('lorenz.html');

@app.route('/numbers')
def numbers():
    return render_template('numbersindex.html')

@app.route('/numbersdoc')
def numbersdoc():
    return render_template('numbersdoc.html')

if __name__ == '__main__':
    "Are we in the __main__ scope? Start test server."
    app.run(debug=True);

