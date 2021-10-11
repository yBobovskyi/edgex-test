import random
import paho.mqtt.client as mqtt
import json
import redis
from datetime import datetime

broker = 'edgex-mqtt-broker'
port = 1883
topic = '/home/laptop'
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker\n');
    else:
        print('Failed to connect to MQTT broker, return code %d\n', rc)

def parse_json(json_str):
    reading = json.loads(json_str)['readings'][0]
    record = {
               'device' : reading['deviceName'],
               'source' : reading['resourceName'],
               'type'   : reading['valueType'],
               'value'  : reading['value'],
               'origin' : datetime.fromtimestamp(int(reading['origin']) / 1000000000)
             }
    return record

def write_record(record):
    r = redis.Redis(host = 'redis', port = 6380, db = 1)
    with r.lock('cpu_redis'):
        r.lpush(record['source'], json.dumps({ 'origin' : record['origin'].strftime("%Y-%m-%d %H:%M:%S"), 'value' : float(record['value']) }))
        if r.llen(record['source']) > 20:
            r.rpop(record['source'])

current_record = {}

def on_message(client, userdata, msg):
    current_record = parse_json(msg.payload.decode())
    if current_record['device'] == 'cpu':
        write_record(current_record)

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.subscribe(topic)
client.loop_forever()
