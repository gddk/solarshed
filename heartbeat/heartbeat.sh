#!/bin/bash

IFS='
'
sleep 30
touch /var/tmp/solarshed.heartbeat.txt
echo "$(date +"%Y-%m-%d %H:%M:%S") $(for i in $(cat /var/tmp/solarshed_controller.last.log); do echo -n " $i"; done)" > /var/tmp/solarshed.heartbeat.txt.1
head -n 1000 /var/tmp/solarshed.heartbeat.txt >> /var/tmp/solarshed.heartbeat.txt.1
/bin/mv /var/tmp/solarshed.heartbeat.txt.1 /var/tmp/solarshed.heartbeat.txt
echo aws s3 cp /var/tmp/solarshed.heartbeat.txt s3://${BUCKET}/heartbeat.txt
aws s3 cp /var/tmp/solarshed.heartbeat.txt s3://${BUCKET}/heartbeat.txt
echo $?

