#!/home/pi/venvs/rpi/bin/python

from ssr.ssr import SSR
import datetime
import os.path
import requests
import socket
import json
import secrets
from mate2.mate2 import Mate2
from temperature.temperature import Temperature
from weather import Weather
from json_cache import write_json_cache, get_json_cache


def is_sunny():
    now = datetime.datetime.now()
    print('now=' + str(now))
    w = Weather(secrets.openweather_api_key, secrets.openweather_lat,
                secrets.openweather_lon)
    weather = w.get_weather()
    if not weather:
        print('No weather data, assume DARK')
        send_graphite('solar.weatherapi.up', 0)
        return False
    else:
        send_graphite('solar.weatherapi.up', 1)
    try:
        outside_temp_f = weather['main']['temp']
        print('outside_temp_f=' + str(outside_temp_f))
        send_graphite('solar.outside_temp_f', outside_temp_f)
        humidity = weather['main']['humidity']
        print('humidity=' + str(humidity))
        send_graphite('solar.humidity', humidity)
        wind_speed = weather['wind']['speed']
        print('wind_speed=' + str(wind_speed))
        send_graphite('solar.wind_speed', wind_speed)
        cloudiness = weather['clouds']['all']
        print('cloudiness=' + str(cloudiness))
        send_graphite('solar.cloudiness', cloudiness)
        sunrise_ts = weather['sys']['sunrise']
        sunrise = datetime.datetime.fromtimestamp(
            sunrise_ts + secrets.sunrise_offset_minutes * 60)
        print('adjusted sunrise=' + str(sunrise))
        sunset_ts = weather['sys']['sunset']
        sunset = datetime.datetime.fromtimestamp(
            sunset_ts - secrets.sunset_offset_minutes * 60)
        print('adjusted sunset=' + str(sunset))
        after_sunrise_seconds = (now - sunrise).total_seconds()
        print('after_sunrise_seconds=' + str(after_sunrise_seconds))
        before_sunset_seconds = (sunset - now).total_seconds()
        print('before_sunset_seconds=' + str(before_sunset_seconds))
        if cloudiness < secrets.cloudiness_threshold and \
                after_sunrise_seconds > 0 and before_sunset_seconds > 0:
            print('SUNNY')
            send_graphite('solar.sunny', 1)
            return True
        else:
            print('DARK')
            send_graphite('solar.sunny', 0)
            return False
    except Exception as e:
        print('Exception occurred in is_sunny, assume DARK: {}'.format(e))
        return False


def get_mate2_status():
    return Mate2(expected_devices=secrets.mate2_devices).getStatus()


def send_graphite(name, value):
    now = datetime.datetime.now()
    msg = '{} {} {}\n'.format(
        name, value, now.strftime('%s'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 2003))
        s.sendall(msg.encode('ascii'))


def grid_mode_always():
    if os.path.isfile('/home/pi/code/rpi/gridmode'):
        with open('/home/pi/code/rpi/gridmode', 'r') as fp:
            raw = fp.read()
            if raw.startswith('ON'):
                return True
    return False


def main():
    ssr1 = SSR(17)
    ssr2 = SSR(27)
    now = datetime.datetime.now(datetime.timezone.utc)
    grid_mode = grid_mode_always()
    grid_on = True if ssr1.state and ssr2.state else False
    sunny = is_sunny()
    t = Temperature()
    send_graphite('solar.temp_f', t.F)
    print('temp_f={}'.format(t.F))
    send_graphite('solar.temp_c', t.C)
    print('temp_c={}'.format(t.C))
    mate2 = {}
    try:
        mate2 = get_mate2_status()
    except Exception as e:
        print('Exception occurred in get_mate2_status() :{}'.format(e))
    if mate2.get('devices', {}).get('B', {}).get(
        'battery_voltage', None) is not None:
        write_json_cache('/tmp/mate2.last.json', mate2)
    else:
        print('WARNING: no mate2 data available, checking if cache is good')
        mate2 = get_json_cache('/tmp/mate2.last.json', 10)

    if not mate2:
        mate2 = {}

    print('mate2=' + json.dumps(mate2))
    bvolts = 0.0
    bvolts_counter = 0
    for key in mate2.get('devices', {}).keys():
        m = mate2['devices'][key]
        if m.get('battery_voltage', None) is not None:
            send_graphite('solar.{}.battery_voltage'.format(key),
                          m['battery_voltage'])
        if m.get('charger_current', None) is not None:
            send_graphite('solar.{}.charger_current'.format(key),
                          m['charger_current'])
        if m.get('pv_input_voltage', None is not None):
            send_graphite('solar.{}.pv_input_voltage'.format(key),
                          m['pv_input_voltage'])
        if m.get('daily_kwh', None) is not None:
            send_graphite('solar.{}.daily_kwh'.format(key),
                          m['daily_kwh'])
        if m.get('daily_amph', None) is not None:
            send_graphite('solar.{}.daily_amph'.format(key),
                          m['daily_amph'])
        if m.get('battery_voltage', None) is not None:
            bvolts_counter += 1
            bvolts = round(
                (bvolts + m['battery_voltage']) / bvolts_counter, 2)
    bvolts = round(bvolts, 1)
    print('bvolts={}'.format(bvolts))
    send_graphite('solar.bvolts', bvolts)
    note = 'no change'
    if not grid_on and (grid_mode or
                        not sunny or
                        bvolts < secrets.low_bvolts
                        ):
        ssr1.on()
        ssr2.on()
        note = 'toggled ON'
        grid_on = True
    elif grid_on and sunny and not grid_mode and bvolts >= secrets.low_bvolts:
        ssr1.off()
        ssr2.off()
        note = 'toggled OFF'
        grid_on = False

    send_graphite('solar.ssr1.state', ssr1.state)
    send_graphite('solar.ssr2.state', ssr2.state)
    print('{} ssr1: {} ssr2: {} {} grid_mode: {}'.format(
        now.strftime('%Y-%m-%dT%H:%M:%S%z'),
        ssr1.state,
        ssr2.state,
        note,
        grid_mode
    ))


if __name__ == '__main__':
    main()
