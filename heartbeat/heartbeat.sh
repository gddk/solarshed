#!/bin/bash

sleep 5
touch /tmp/heartbeat.txt
echo "$(date +"%Y-%m-%d %H:%M:%S") $(cat /tmp/7_temperature.last.log | egrep -o "solar.temp_. [0-9.]*" | tr '\n' ' ')ssr_state: $(/home/pi/code/rpi/ssr/ssr_state.py)$(if [[ "ON" == "$(cat /home/pi/code/rpi/gridmode)" ]]; then echo " gridmode"; fi)" > /tmp/heartbeat.txt.1
head -n 5000 /tmp/heartbeat.txt >> /tmp/heartbeat.txt.1
/bin/mv /tmp/heartbeat.txt.1 /tmp/heartbeat.txt
echo /usr/bin/aws s3 cp /tmp/heartbeat.txt s3://${BUCKET}/heartbeat.txt
/usr/bin/aws s3 cp /tmp/heartbeat.txt s3://${BUCKET}/heartbeat.txt
echo $?

