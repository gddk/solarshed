#!/home/pi/venvs/rpi/bin/python

from ssr.ssr import SSR
import datetime
import os.path
import requests
import socket
import secrets


def is_sunny():
    now = datetime.datetime.now()
    print('now=' + str(now))
    weather = get_weather()
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


def get_weather():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    url += '?lat={}&lon={}&units=imperial&appid={}'.format(
        secrets.openweather_lat, secrets.openweather_lon,
        secrets.openweather_api_key)
    data = {}
    try:
        resp = requests.get(url)
        data = resp.json()
    except Exception as e:
        print('Error occurred getting weather: {}'.format(e))
        return None
    return data


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
