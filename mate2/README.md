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

b'\nC,00,27,15,107,005,08,03,000,01,562,0009,00,081\r'

1. ASCII (10) New Line character denoting the start of the status page.
2. MX/FM address.
3. ASCII (44) a comma as a data separator.
4. Unused, ASCII (48).
5. Unused, ASCII (48). 
6. ASCII (44) a comma as a data separator. 
7. Tens digit of Charger current. 
8. Ones digit of Charger current. 
9. ASCII (44) a comma as a data separator. 
10. Tens digit of PV current. 
11. Ones digit of PV current. 
12. ASCII (44) a comma as a data separator. 
13. Hundreds digit of the PV input voltage. 
14. Tens digit of PV input voltage. 
15. Ones digit of PV input voltage. 
16. ASCII (44) a comma as a data separator. 
17. Tens digit of Daily kWH. 
18. Ones digit of Daily kWH. 
19. Tenths digit of Daily kWH. 
20. ASCII (44) a comma as a data separator. 
21. Unused, ASCII (48). 
22. Tenths of amp Charger current (FM80 / FM60 only) 
23. ASCII (44) a comma as a data separator. 
24. High byte of Aux mode. 
25. Low byte of Aux mode. 
26. ASCII (44) a comma as a data separator. 
27. High byte of Error mode. 
28. Middle byte of Error mode. 
29. Low byte of Error mode. 
30. ASCII (44) a comma as a data separator. 
31. High byte of charger mode. 
32. Low byte of charger mode. 
33. ASCII (44) a comma as a data separator
34. Tens digit of battery voltage. 
35. Ones digit of battery voltage. 
36. Tenths digit of battery voltage. 
37. ASCII (44) a comma as a data separator. 
38. Thousands digit of daily AH. 
39. Hundreds digit of daily AH. 
40. Tens digit of daily AH. 
41. Ones digit of daily AH. 
42. ASCII (44) a comma as a data separator. 
43. Unused, ASCII (48). 
44. Unused, ASCII (48). 
45. ASCII (44) a comma as a data separator. 
46. Hundredths digit of Chksum. 
47. Tens digit of Chksum. 
48. Ones digit of Chksum. 
49. ASCII (13) carriage return. Denotes end of status page.


Taking this ^ information to translate into a dict like this:

```
status[str(line[1:2])] = {
                'battery_voltage': float(line[33:36]) / 10.0,
                'charger_current': float(line[6:8] + line[21:22]) / 10.0,
                'pv_input_voltage': int(line[12:15]),
                'daily_kwh': float(line[16:19]) / 10.0
                'daily_amph': float(line[37:41])
            }
```

The comm manual PDF also says:

> In addition to a LCD and buttons for display and control, an OutBack Mate provides an isolated RS232 port for PC communication in the form of a female DB9 connector, running at a baud rate of 19200, 8 bits, no parity, 1 stop bit. The Mates’ serial port is optically isolated from the rest of the OutBack products it is connected too. This isolation requires that the Mate ‘steals’ power from the PC in order to communicate. Figure 2 shows which lines of a standard PCs serial port are used. All pin numbers and names are referenced from the PC.

> The Mate requires that the DTR (pin 4) be driven high (set) and that RTS (pin 7) be driven low (cleared), in order to power the port. The Mate transmits data on the RX (pin 2) line, and listens for commands on the TX (pin 3) line. GND (pin 5) is ground. No other pins are used by the Mate.

This is all critical information to get communication to work

[CableCreation 6.6 Feet USB to RS232 Adapter with PL2303 Chipset, Gold Plated USB 2.0 to DB9 Serial Converter Cable Support Cashier Register, Modem, Scanner, Digital Cameras,CNC etc, 2M /Black ](https://www.amazon.com/gp/product/B0758BWVXF/)

## Reading MATE2 with miniterm

```
 miniterm --dtr 1 --rts 0 --encoding ascii --raw /dev/ttyUSB0 19200
--- forcing DTR active
--- forcing RTS inactive
--- Miniterm on /dev/ttyUSB0  19200,8,N,1 ---
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---

C,00,33,17,111,011,01,03,000,02,544,0019,00,067
C,00,33,16,111,011,01,03,000,02,544,0019,00,066
```
