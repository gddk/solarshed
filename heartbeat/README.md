# heartbeat

Alert when raspberry pi stops working

## cron

This entry from [../cron.d/rpi](../cron.d/rpi) pushes the heartbeat.txt file to AWS every 5 minutes.

```
*/5 * * * * pi BUCKET=yourBucket /home/pi/code/rpi/heartbeat/heartbeat.sh >/tmp/heartbeat.last.log 2>&1
```

The idea is then to monitor the timestamp on this file in AWS S3 using a lambda that will alert if too old.

# S3

Create a BUCKET and make a role that will allow full read/write access.

By putting a little data in heartbeat.txt, you can monitor the contents of the file too, if you want. We're not doing that, yet, just monitoring the Last-Modified attribute of the file, however, its convenient to check the contents of the file manually using the AWS Console. When opening the heartbeat.txt file in AWS Console, it's convenient that the most recent data is at the top of the file; no scrolling to the bottom required.

## Lambda 

See [lambda_function.py](lambda_function.py) - this will check the Last-Modified of the heartbeat.txt file in the S3 Bucket and alert to PagerDuty if too old.

## CloudWatch Event

Setup a CloudWatch Event to run every 5 minutes to trigger the Lambda function

