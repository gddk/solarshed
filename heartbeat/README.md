# heartbeat

Alert when raspberry pi stops working

## Heartbeat monitoring

/etc/cron.d/heartbeat

```
* * * * * pi BUCKET=yourbucket /home/pi/code/rpi/heartbeat/heartbeat.sh &>/dev/null
```

The idea is then to monitor the timestamp on this file in AWS S3 using a lambda that will alert if too old.


## Generate payload.json
```
cat pagerduty_payload.json | sed -e "s/##NOW##/$(date +"%Y-%m-%dT%T.%3N%z")/" -e "s/##LAST##/$(tail -n 1 /tmp/heartbeat.txt)/" > payload.json"
```
