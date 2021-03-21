#!/home/pi/venvs/rpi/bin/python

from ssr.ssr import SSR
import time
import datetime
import os.path


def is_sunny():
    now = datetime.datetime.now(datetime.timezone.utc)
    hour = int(now.strftime('%H'))
    if hour > 15 and hour < 23:
        return True
    else:
        return False

def grid_mode_always():
    if os.path.isfile('/home/pi/code/rpi/gridmode'):
        with open('/home/pi/code/rpi/gridmode', 'r') as fp:
            raw = fp.read()
            if raw.startswith('ON'):
                return True
    return False

def get_battery_voltage():
    # todo: fetch the real voltage
    return 52.1

def main():
    ssr1 = SSR(17)
    ssr2 = SSR(27)
    now = datetime.datetime.now(datetime.timezone.utc)
    grid_mode = grid_mode_always()
    grid_on = True if ssr1.state and ssr2.state else False
    sunny = is_sunny()
    bvolts = get_battery_voltage()
    note = 'no change'
    if not grid_on and (grid_mode or
                        not sunny or
                        bvolts < 50.1
                        ):
        ssr1.on()
        ssr2.on()
        note = 'toggled ON'
        grid_on = True
    elif grid_on and sunny and not grid_mode and bvolts >= 50.1:
        ssr1.off()
        ssr2.off()
        note = 'toggled OFF'
        grid_on = False

    print('{} ssr1: {} ssr2: {} {} grid_mode: {}'.format(
        now.strftime('%Y-%m-%dT%H:%M:%S%z'),
        ssr1.state,
        ssr2.state,
        note,
        grid_mode
    ))

if __name__ == '__main__':
    main()
