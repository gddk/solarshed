#!/bin/bash

raw_c=$(cat /sys/bus/w1/devices/28*/w1_slave | egrep -o 't=[0-9]*' | sed -e 's/t=//')
if [[ "$raw_c" ]]; then
  temp_c=$(echo "scale=2; ($raw_c/1000)" | bc)
  temp_f=$(echo "scale=2; ($raw_c/1000) * 9.0 / 5.0 + 32" | bc)
  val_c="solar.temp_c $temp_c $(date +%s)"
  val_f="solar.temp_f $temp_f $(date +%s)"
  echo "$(date +"%Y-%m-%d %H:%M") $val_f"
  echo "$(date +"%Y-%m-%d %H:%M") $val_c"
  echo $val_f | nc -N localhost 2003
  echo $val_c | nc -N localhost 2003
else
  echo "Error: could not read temperature"
  exit 1
fi
