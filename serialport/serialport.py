import serial

port0 = serial.Serial(
        "/dev/ttyAMA0",
        baudrate=19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

while True:
    rcv0 = port0.read(49)
    print('rcv0=' + str(rcv0))


