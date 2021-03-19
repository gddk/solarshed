#!/bin/bash

sleep 5
touch /tmp/heartbeat.txt
tail -n 5000 /tmp/heartbeat.txt > /tmp/heartbeat.txt.1
echo "$(date +"%Y-%m-%d %H:%M:%S") $(cat /tmp/7_temperature.last.log | egrep -o "solar.temp_. [0-9.]*" | tr '\n' ' ')" >> /tmp/heartbeat.txt.1
/bin/mv /tmp/heartbeat.txt.1 /tmp/heartbeat.txt
echo /usr/bin/aws s3 cp /tmp/heartbeat.txt s3://${BUCKET}/heartbeat.txt
/usr/bin/aws s3 cp /tmp/heartbeat.txt s3://${BUCKET}/heartbeat.txt
echo $?

