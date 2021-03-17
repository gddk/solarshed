#!/bin/bash

t=$(/home/pi/code/rpi/7_temperature/7_temperature.py)
val_f="solar.temp_f $(echo $t | egrep -o '^[0-9.]*') $(date +%s)";
val_c="solar.temp_c $(echo $t | egrep -o '[0-9.]*C$' | sed -e 's/C//') $(date +%s)"
echo "$(date +"%Y-%m-%d %H:%M") $val_f"
echo "$(date +"%Y-%m-%d %H:%M") $val_c"
echo $val_f | nc -N localhost 2003
echo $val_c | nc -N localhost 2003
