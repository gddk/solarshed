#!/bin/bash

IFS='
'
sleep 5
touch /tmp/heartbeat.txt
echo "$(date +"%Y-%m-%d %H:%M:%S") $(cat /tmp/7_temperature.last.log | egrep -o "solar.temp_. [0-9.]*" | tr '\n' ' ')$(for i in $(cat /tmp/solarshed_controller.last.log); do echo -n " $i"; done)" > /tmp/heartbeat.txt.1
head -n 1000 /tmp/heartbeat.txt >> /tmp/heartbeat.txt.1
/bin/mv /tmp/heartbeat.txt.1 /tmp/heartbeat.txt
echo /usr/bin/aws s3 cp /tmp/heartbeat.txt s3://${BUCKET}/heartbeat.txt
/usr/bin/aws s3 cp /tmp/heartbeat.txt s3://${BUCKET}/heartbeat.txt
echo $?

