#!/usr/bin/bash

docker-compose up -d device-cpu
docker-compose up -d mqtt-broker
docker-compose up -d app-service-mqtt
docker-compose up -d flask
docker-compose up -d mqtt-redis-parser
docker-compose up -d command
docker-compose up -d app-service-rules
docker-compose up -d rulesengine
docker-compose up -d switch-mock
docker-compose up -d device-switch

curl -X POST \
  http://localhost:59720/streams \
  -H 'Content-Type: application/json' \
  -d '{"sql": "create stream demo() WITH (FORMAT=\"JSON\", TYPE=\"edgex\")"}'

curl -X POST \
  http://localhost:59720/rules \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "rule1",
  "sql": "SELECT core0temp FROM demo WHERE core0temp > 100.0",
  "actions": [
    {
      "rest": {
        "url": "http://edgex-core-command:59882/api/v2/device/name/switch/switch",
        "method": "put",
        "dataTemplate": "{\"state\":\"OFF\"}",
        "sendSingle": true
      }
    },
    {
      "log":{}
    }
  ]
}'
