#!/home/pi/venvs/rpi/bin/python
from ssr import SSR

ssr1 = SSR(17)
ssr2 = SSR(27)

ssr1.on()
ssr2.on()

print('{} {}'.format(ssr1.state, ssr2.state))
