#!/bin/bash

touch /tmp/heartbeat.txt
tail -n 5000 /tmp/heartbeat.txt > /tmp/heartbeat.txt.1
date +"%Y-%m-%d %H:%M:%S" >> /tmp/heartbeat.txt.1
/bin/mv /tmp/heartbeat.txt.1 /tmp/heartbeat.txt
aws s3 cp /tmp/heartbeat.txt s3://${BUCKET}/heartbeat.txt

