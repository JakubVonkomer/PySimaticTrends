# PySimaticTrends
A small Python application for making charts from Simatic Basic Panels txt logs, which can be stored on a external USB drive
named as Data_log0.txt to Data_logXY.txt .
in the format:

"VarName"	"TimeString"	"VarValue"	"Validity"	"Time_ms"
"Variable1"	"2012-01-03 22:41:14"	0.000000	1	40911945303.865738
"Variable2"	"2012-01-03 22:41:14"	0.000000	1	40911945303.935188
...

Also, it can read binary DTL files stored by Weintek panels.

This program requires Python 3.6+ and uses matplotlib to draw the charts.
