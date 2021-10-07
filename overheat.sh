#!/usr/bin/bash

curl -X POST -H "Content-Type:text/plain" http://$1:59986/api/v2/resource/cpu/core$2temp -d $3
