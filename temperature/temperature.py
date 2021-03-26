import glob
import time


class Temperature:

    def __init__(self, cache_seconds=60):
        self.last_load = None
        self.cache_seconds = cache_seconds
        device_folder = glob.glob('/sys/bus/w1/devices/28*')[0]
        self.device_file =  device_folder + '/w1_slave'
        self._load()

    def get_C(self):
        self._load()
        return self._temp_c

    def get_F(self):
        return round(self.get_C() * 9.0 / 5.0 + 32.0, 2)

    def _load(self):
        if self.last_load is None or \
                self.last_load + self.cache_seconds < int(time.time()):
            self._read_c()
            self.last_load = int(time.time())

    def _read_c(self):
        raw = ''
        with open(self.device_file, 'r') as f:
            raw = f.read()
        pos = raw.find('t=')
        if pos == -1:
            raise ValueError('Could not read the temperature')
        temp_str = raw[pos+2:]
        self._temp_c = float(temp_str) / 1000.0

    C = property(get_C)
    F = property(get_F)
