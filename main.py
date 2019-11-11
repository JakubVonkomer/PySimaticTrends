import sys
import os

import version as vs
from file_dialog import openFileDialog
import config as cfg
import simatic_files as sf
import weintek_files as wf

from make_trends import *

print (vs.appName + ' ' + vs.version)
print ('')

#print (sys.argv)

# argv[1] je nazov suboru na otvorenie
if len(sys.argv) > 1:
    filename = sys.argv[1]
elif(cfg.ASK_FOR_FILENAME):
    #filename = input("Enter file name: ")
    filename = openFileDialog()
else:
    # napevno
    filename = cfg.FIXED_FILENAME

print("Opening filename ",filename)

#detekcia typu
name, ext = os.path.splitext(filename)
resultOK = False
if(ext == '.txt'): # Simatic Basic Panel TXT file
    resultOK = sf.OpenSimaticTXTFile(filename)
elif(ext == '.dtl'): # Weintek binary DTL files
    resultOK = wf.OpenWeintekDtlFile(filename)
else:
    print('Error: Unsupported file type ',ext)

if(resultOK):
    plot_all(cfg.ALL_VARIABLES_IN_SINGLE_TREND) # vykresli grafy

#zatvorenie suboru


#koniec
print('-----------------------------------------')
print('(c) 2019 by VONSCH s.r.o.')
# keby sme chceli podrzat konzolu
#input('Press Enter to exit')
