# heartbeat

Alert when raspberry pi stops working

## Heartbeat monitoring

/etc/cron.d/heartbeat

```
* * * * * pi BUCKET=yourbucket /home/pi/code/rpi/heartbeat/heartbeat.sh &>/dev/null
```

NOTE: all cron entries are in [../cron.d/rpi](../cron.d/rpi)

The idea is then to monitor the timestamp on this file in AWS S3 using a lambda that will alert if too old.

## Lambda 

See lambda_function.py

