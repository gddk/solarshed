# mate2

## Usage

```
from mate2 import Mate2


mate2 = Mate2()
status = mate2.getStatus()
print('{}'.format(status))

status_json_str = mate2.getStatus(format='json')
print('{}'.format(status_json_str))
```

and the output looks like this:
```
>>> from mate2 import Mate2
>>>
>>>
>>> mate2 = Mate2()
>>> status = mate2.getStatus()
lines=['\nC,00,03,01,112,000,00,03,000,02,556,0001,00,049', '\nC,00,03,01,112,000,00,03,000,02,556,0001,00,049', '']
line=
C,00,03,01,112,000,00,03,000,02,556,0001,00,049
line=
C,00,03,01,112,000,00,03,000,02,556,0001,00,049
>>> print('{}'.format(status))
{'C': {'battery_voltage': 55.6, 'charger_current': 3, 'ac_input_voltage': 112, 'ac_output_voltage': 0}}
>>>
>>> status_json_str = mate2.getStatus(format='json')
lines=['\nC,00,02,01,112,000,09,03,000,02,556,0001,00,057', '\nC,00,03,01,113,000,00,03,000,02,556,0001,00,050', '']
line=
C,00,02,01,112,000,09,03,000,02,556,0001,00,057
line=
C,00,03,01,113,000,00,03,000,02,556,0001,00,050
>>> print('{}'.format(status_json_str))
{"C": {"battery_voltage": 55.6, "charger_current": 3, "ac_input_voltage": 113, "ac_output_voltage": 0}}
```

### Run from command line:
```
python mate2.py
lines=['\nC,00,02,01,114,000,09,03,000,02,558,0001,00,061', '\nC,00,02,01,114,000,09,03,000,02,558,0001,00,061', '']
line=
C,00,02,01,114,000,09,03,000,02,558,0001,00,061
line=
C,00,02,01,114,000,09,03,000,02,558,0001,00,061
{"C": {"battery_voltage": 55.8, "charger_current": 2, "ac_input_voltage": 114, "ac_output_voltage": 0}}

# if this ^ is too noisy, try this:
python mate2.py | tail -n 1 | jq
{
  "C": {
    "battery_voltage": 55.8,
    "charger_current": 2,
    "ac_input_voltage": 113,
    "ac_output_voltage": 0
  }
}


```

## Mate Serial Communications Guide, MX/FM Status Page

REF: https://www.wmrc.edu/projects/BARenergy/manuals/outback-manuals/Mate_Serial_Comm_R302.pdf

Mate Code Revs. of 4.00 and greater

> The status page the Mate emits for each MX connected is 49 Bytes long. Referring to the Figure 9 the byte definitions are as follows:

b'\nC,4:00,7:00,10:00,13:029,17:004,21:00,24:03,27:000,31:00,34:527,38:0008,00,059'

1. ASCII (10) New Line character denoting the start of the status page.
2. This is the Inverter address.

3. ASCII (44) a comma as a data separator.

4. Tens digit of Inverter current.
5. Ones digit of Inverter current.

6. ASCII (44) a comma as a data separator.

7. Tens digit of Charger current..
8. Ones digit of Charger current.

9. ASCII (44) a comma as a data separator.

10. Tens digit of Buy current..
11. Ones digit of Buy current.

12. ASCII (44) a comma as a data separator.

13. Hundreds digit of the AC input voltage.
14. Tens digit of AC input voltage.
15. Ones digit of AC input voltage.

16. ASCII (44) a comma as a data separator.

17. Hundreds digit of the AC output voltage.
18. Tens digit of AC output voltage.
19. Ones digit of AC output voltage.

20. ASCII (44) a comma as a data separator.

21. Tens digit of Sell current.
22. Ones digit of Sell current.

23. ASCII (44) a comma as a data separator.

24. Tens digit of FX operating mode.
25. Ones digit of FX operating mode.

26. ASCII (44) a comma as a data separator.

27. High byte of FX Error mode.
28. Middle byte of FX Error mode.
29. Low byte of FX Error mode.

30. ASCII (44) a comma as a data separator.

31. High byte of FX AC mode.
32. Low byte of FX AC mode

33. ASCII (44) a comma as a data separator.

34. Tens digit of FX battery voltage.
35. Ones digit of FX battery voltage.
36. Tenths digit of FX battery voltage.

37. ASCII (44) a comma as a data separator.

38. High byte of FX Misc.
39. Middle byte of FX Misc.
40. Low byte of FX Misc.

41. ASCII (44) a comma as a data separator.

42. High byte of FX Warning mode.
43. Middle byte of FX Warning mode.
44. Low byte of FX Warning mode.

45. ASCII (44) a comma as a data separator.

46. Hundreds digit of Chksum.
47. Tens digit of Chksum.
48. Ones digit of Chksum.
49. ASCII (13) carriage return. Denotes end of status page.

It also says:

> In addition to a LCD and buttons for display and control, an OutBack Mate provides an isolated RS232 port for PC communication in the form of a female DB9 connector, running at a baud rate of 19200, 8 bits, no parity, 1 stop bit. The Mates’ serial port is optically isolated from the rest of the OutBack products it is connected too. This isolation requires that the Mate ‘steals’ power from the PC in order to communicate. Figure 2 shows which lines of a standard PCs serial port are used. All pin numbers and names are referenced from the PC.

> The Mate requires that the DTR (pin 4) be driven high (set) and that RTS (pin 7) be driven low (cleared), in order to power the port. The Mate transmits data on the RX (pin 2) line, and listens for commands on the TX (pin 3) line. GND (pin 5) is ground. No other pins are used by the Mate.

This is all critical information to get communication to work

[CableCreation 6.6 Feet USB to RS232 Adapter with PL2303 Chipset, Gold Plated USB 2.0 to DB9 Serial Converter Cable Support Cashier Register, Modem, Scanner, Digital Cameras,CNC etc, 2M /Black ](https://www.amazon.com/gp/product/B0758BWVXF/)

```
miniterm --dtr 1 --rts 0 --encoding ascii --raw /dev/ttyUSB0 19200
--- forcing DTR active
--- forcing RTS inactive
--- Miniterm on /dev/ttyUSB0  19200,8,N,1 ---
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---

C,00,00,00,029,004,00,03,000,00,529,0008,00,061
C,00,00,00,029,004,00,03,000,00,529,0008,00,061
C,00,00,00,029,004,00,03,000,00,529,0008,00,061
C,00,00,00,029,004,00,03,000,00,529,0008,00,061
C,00,00,00,029,004,00,03,000,00,529,0008,00,061
C,00,00,00,029,004,00,03,000,00,529,0008,00,061

```
