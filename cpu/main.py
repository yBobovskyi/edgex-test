from cpu import *
import time
import requests

resource_endpoint = 'http://192.168.0.104:59986/api/v2/resource/cpu/'

while True:
    cpu_temps = get_cpu_temps()
    i = 0
    for temp in cpu_temps:
        requests.post(resource_endpoint + 'core' + str(i) + 'temp', data = str(temp), headers =  { 'Content-Type' : 'text/plain' })
        i += 1
    time.sleep(5)