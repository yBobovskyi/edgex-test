#!/usr/bin/bash

curl -X PUT -H "Content-Type: application/json" http://localhost:59882/api/v2/device/name/switch/switch -d '{ "state" : "ON" }'
