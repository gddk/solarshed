#!/home/pi/venvs/temperature/bin/python

from temperature import Temperature

t = Temperature(30)
print('%sF, %sC' % (t.F, t.C))

