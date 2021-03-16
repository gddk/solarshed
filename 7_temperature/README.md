# 7_temperature

Making SunFounder DS18B20 Temperature Sensor Module for Arduino and Raspberry Pi work

## References

REF: https://www.amazon.com/gp/product/B013GB27HS/
REF: https://thepihut.com/blogs/raspberry-pi-tutorials/gpio-and-python-79-temperature-sensor

## Do this first to get the I2C working in 1 wire mode

```
sudo raspi-config
# Interfacing Options
# I2C
# Yes

sudo vim /boot/config.txt 
# add this to the bottom without the #
#dtoverlay=w1-gpio

sudo shutdown -h now
```

## Now wire up like this

![SunFounder DS18B20 Wired to Rasberry Pi 4](7_temperature.png "SunFounder DS18B20 Wired to Rasberry Pi 4")

## Setup python3 Virtual Env

```
cd
mkdir -p venvs
cd venvs
python3 -m venv temperature
souuce temperature/bin/activate
```

## Clone this repo

```
cd
mkdir -p code
cd code
git clone https://github.com/gddk/rpi.git
cd rpi/7_temperature
```

## Run the code
```
(temperature) pi@raspberrypi:~/code/temperature $ ./7_temperature.py
66.99F, 19.44C
```
