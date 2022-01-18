#!/bin/bash

IFS='
'

if [[ "$BUCKET" == "" ]]; then
  echo "ERROR: no BUCKET"
  echo "Usage: BUCKET=\"YourS3BucketName\" /home/pi/code/solarshed/backup/grafana.sh"
  exit 2
fi
sleep 30
d="$(date +"%Y-%m-%y-%H-%M")-grafana"
echo $d
sudo docker commit -p graphite "$d"
sudo docker save -o /tmp/${d}.tar $d
sudo docker image rm $d
cd /tmp
sudo tar czf ${d}.tar.gz ${d}.tar
sudo rm -f $d
ls -lah ${d}.tar.gz
echo aws s3 cp /tmp/${d}.tar.gz s3://${BUCKET}/${d}.tar.gz
aws s3 cp /tmp/${d}.tar.gz s3://${BUCKET}/${d}.tar.gz
echo $?
sudo rm -f /tmp/${d}.tar.gz
