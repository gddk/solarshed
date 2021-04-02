import requests
from json_cache import write_json_cache, get_json_cache


class Weather:
    def __init__(self, api_key, lat, lon,
                 cache_file='/tmp/weather.last.json', cache_minutes=30):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.cache_file = cache_file
        self.cache_minutes = cache_minutes

    def get_weather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather'
        url += '?lat={}&lon={}&units=imperial&appid={}'.format(
            self.lat, self.lon, self.api_key)
        data = {}
        try:
            resp = requests.get(url)
            data = resp.json()
        except Exception as e:
            self.warning = 'WARNING: Exception getting weather: {}'.format(e)

        if data.get('clouds', None) is not None:
            write_json_cache(self.cache_file, data)
            return data
        else:
            self.warning = 'WARNING: no weather data available, check cache...'
            return get_json_cache(self.cache_file, self.cache_minutes)


if __name__ == '__main__':
    import json
    import secrets
    w = Weather(secrets.openweather_api_key, secrets.openweather_lat,
                secrets.openweather_lon, cache_file='/dev/null',
                cache_minutes=-1)
    weather = w.get_weather()
    if weather:
        print(json.dumps(weather))
    else:
        print(w.warning)

