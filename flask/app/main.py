import redis
import json
from flask import Flask, request
from datetime import datetime
import requests

app = Flask(__name__)
requests.post('http://edgex-support-notifications:59860/api/v2/subscription', data = '[ { "apiVersion": "v2", "subscription": { "name": "subscriptionA", "channels": [ { "type": "REST", "host": "edgex-flask", "port": 5000, "path": "/notifications/data", "httpMethod": "POST" } ], "categories": [ "temperature" ], "receiver": "receiverA", "adminState": "UNLOCKED" } } ]')

def cpu_records():
    r = redis.Redis(host = 'redis', port = 6380, db = 1)
    out_str = '<table border="1"><tr><th style="width:100px">CPU</th><th>Core 0</th><th style="width:250px">Time</th><th>Core 1</th><th style="width:250px">Time</th><th>Core 2</th><th style="width:250px">Time</th><th>Core 3</th><th style="width:250px">Time</th></tr>'
    temps = []
    lock = r.lock('cpu_redis')
    lock.acquire(blocking = True)
    for i in range(4):
        temps.append([])
        source = 'core' + str(i) + 'temp'
        for j in range(r.llen(source)):
            temps[i].append(json.loads(r.lindex(source, j)))
    lock.release()

    lengths = [len(temps[i]) for i in range(4)]
    for i in range(min(lengths)):
        out_str += '<tr><td></td>'
        for j in range(len(temps)):
            out_str += '<td style="text-align:center">' + str(temps[j][i]['value']) + '</td><td style="text-align:center">' + temps[j][i]['origin'] + '</td>'
        out_str += '</tr>'
    out_str += '</table>'
    out_str += '<table><tr><th>Average:</th><th></th></tr>'
    for i in range(len(temps)):
        out_str += '<tr><td>Core ' + str(i) + ':</td><td>'
        if len(temps[i]) > 0:
            out_str += str(sum(float(temp['value']) for temp in temps[i]) / len(temps[i]))
        out_str += '</td></tr>'
    out_str += '</table>'

    return out_str

@app.route('/')
def show_records():
    str = '<meta http-equiv="refresh" content="5">'
    str += cpu_records()
    str += '</meta>'
    return str

def write_record(record):
    r = redis.Redis(host = 'redis', port = 6380, db = 1)
    lock = r.lock('cpu_redis')
    lock.acquire(blocking = True)
    r.lpush(record['source'], json.dumps({ 'origin' : record['origin'].strftime("%Y-%m-%d %H:%M:%S"), 'value' : float(record['value']) }))
    if r.llen(record['source']) > 20:
        r.rpop(record['source'])
    lock.release()

@app.route('/data', methods = ['POST'])
def gather_data():
    data = request.get_json()['readings'][0]
    record = {
               'device' : data['deviceName'],
               'source' : data['resourceName'],
               'type'   : data['valueType'],
               'value'  : data['value'],
               'origin' : datetime.fromtimestamp(int(data['origin']) / 1000000000)
             }
    write_record(record)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/notifications/data', methods = ['POST'])
def gather_notification():
    msg = request.get_data(as_text=True)
    time = datetime.now()
    r = redis.Redis(host = 'redis', port = 6380, db = 2)
    r.lpush('notifications', json.dumps({ 'time' : time.strftime("%Y-%m-%d %H:%M:%S"), 'message' : msg }))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/notifications')
def show_notifications():
    out_str = '<meta http-equiv="refresh" content="5">'
    out_str += '<table border="1"><tr><th>Time</th><th>Message</th></tr>'
    r = redis.Redis(host = 'redis', port = 6380, db = 2)
    for i in range(r.llen('notifications')):
        record = json.loads(r.lindex('notifications', i))
        out_str += '<tr><td>' + record['time']  + '</td><td>' + record['message'] + '</td></tr>'
    out_str += '</table></meta>'
    return out_str
