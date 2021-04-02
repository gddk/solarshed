import json
import os.path
import datetime


def write_json_cache(file, data):
    with open(file, 'w') as fp:
        fp.write(json.dumps(data))


def get_json_cache(file, if_minutes):
    if os.path.isfile(file):
        now = datetime.datetime.now()
        last_mod_ago = (now - datetime.datetime.fromtimestamp(
            os.path.getmtime(file))).total_seconds()
        raw = None
        if last_mod_ago < if_minutes * 60:
            with open(file, 'r') as fp:
                raw = fp.read()
        if raw:
            data = json.loads(raw)
            print('WARNING: using {}'.format(file))
            return data
    return None
