openweather_api_key = 'your key from openweathermap.org'
openweather_lat = 'your_lat'
openweather_lon = 'your_lon'

# This how long after/before sunrise/sunset is it sunny on your panels
sunrise_offset_minutes = 120
sunset_offset_minutes = 90

# 60 means if it's >60% cloudy then it's not sunny
# Set to 101 to make cloudiness not a factor. This could be useful
# if you just want to make low_bvolts be the primary factor
cloudiness_threshold = 75

# This is how many devices you have connected to the mate2
mate2_devices = 2

# If the battery voltage drops below this, toggle grid on
low_bvolts = 49.9
