import serial
import json

class Mate2:

    def __init__(self, device='/dev/ttyUSB0', baudrate=19200,
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS, timeout=2, rts=False, dtr=True,
                 readbytes=48):
        self.device = device
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.rts = rts
        self.dtr = dtr
        self.readbytes = readbytes

    def getStatus(self, format='code'):
        raw = self._getStatusRaw().decode('ascii')
        stats = {
            'battery_voltage': float(raw[33:36]) / 10.0,
            'charger_current': int(raw[6:8]),
            'ac_input_voltage': int(raw[12:15]),
            'ac_output_voltage': int(raw[16:19])
        }
        if format == 'json':
            return json.dumps(stats)
        return stats

    def _getStatusRaw(self):
        port = serial.Serial(
            self.device,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize,
            timeout=self.timeout)
        port.setRTS(self.rts)
        port.setDTR(self.dtr)
        return port.read(self.readbytes)


if __name__ == '__main__':
    print(Mate2().getStatus(format='json'))
