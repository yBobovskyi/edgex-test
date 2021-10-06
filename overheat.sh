#!/usr/bin/bash

curl -X POST -H "Content-Type:text/plain" http://192.168.0.104:59986/api/v2/resource/cpu/core$1temp -d $2
