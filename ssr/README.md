# SSR

## write to graphite

```
echo "* * * * * pi /home/pi/code/solarshed/ssr/ssr_write_state.py > /dev/null 2>&1" | sudo tee /etc/cron.d/ssr_write_state
```
