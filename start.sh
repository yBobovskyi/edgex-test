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
