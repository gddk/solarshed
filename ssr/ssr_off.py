#!/home/pi/venvs/solarshed/bin/python
from ssr import SSR

ssr1 = SSR(17)
ssr2 = SSR(27)

ssr1.off()
ssr2.off()

print('{} {}'.format(ssr1.state, ssr2.state))
