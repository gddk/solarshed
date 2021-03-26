# serialport

```
python3 mate2.py
b'\nC,00,00,00,029,004,00,03,000,00,527,0008,00,059'
```

## Mate Serial Communications Guide, MX/FM Status Page

REF: https://www.wmrc.edu/projects/BARenergy/manuals/outback-manuals/Mate_Serial_Comm_R302.pdf

Mate Code Revs. of 4.00 and greater

The status page the Mate emits for each MX connected is 49 Bytes long. Referring to the Figure 9 the byte definitions are as follows:

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


```
miniterm --dtr 1 --rts 0 --encoding ascii --raw /dev/ttyUSB0 19200

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
