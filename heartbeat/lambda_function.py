import json
from urllib import request
import boto3
import datetime

print('Loading function')

s3 = boto3.client('s3')

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    bucket = 'solarshed'
    key = 'heartbeat.txt'
    try:
        alert = None
        response = s3.get_object(Bucket=bucket, Key=key)
        last_mod = response.get("LastModified")
        now = datetime.datetime.now(datetime.timezone.utc)

        if not last_mod:
            alert = 'last_mod not found'
        elif int((now - last_mod).total_seconds()) > 60 * 30:
            alert = 'WARNING: It has been more than 30 minutes, ' + str(
                int((now - last_mod).total_seconds()/60))
        else:
            print('OK: ' + str(int((now - last_mod).total_seconds()/60)))
            return True
        print(alert)
        lines = response.get('Body').read().decode('utf-8').split('\n')
        last_line = ', '.join(lines[len(lines)-2:])
        last_mod_str = 'not found'
        if last_mod:
            last_mod_str = last_mod.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        data = {
            "payload": {
                "summary": "Solar Shed Heartbeat Alert",
                "timestamp": now.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                "source": "solarshed.localhost",
                "severity": "critical",
                "component": "heartbeat",
                "group": "solar-shed",
                "class": "heartbeat",
                "custom_details": {
                  "last_line": last_line,
                  "last_modified": last_mod_str
                }
            },
            "routing_key": "your routing key",
            "event_action": "trigger",
            "client": "AWS Lambda"
        }

        url = 'https://events.pagerduty.com/v2/enqueue'
        headers = {'Content-Type':'application/json'}
        bindata = json.dumps(data).encode('utf-8')
        req = request.Request(url, bindata, headers)
        resp = request.urlopen(req)
        print(resp.read());
        print(resp.getheaders());

        return True
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

