import sys
#import os
import parseline as PL
import version as vs
from file_dialog import openFileDialog
import config as cfg

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

#Otvorenie suboru
try:
    fp = open(filename, "r" ,encoding='utf-16') #treba dat to utf-16, inak masaker

# obsluha chyby
#except FileNotFoundError:
except Exception as e:
    print(e)
    sys.exit() #ukoncenie skriptu

# parsing file    
i = 0
for line in fp:

    # kontrola na IGNORE_VARNAMES
    ignored_line = [line.find(ignoreVarname1) for ignoreVarname1 in cfg.IGNORE_VARNAMES]
    if(i > 0 and (not 1 in ignored_line)):
        PL.parseline(line) # jadro
    i=i+1

    # kontrola maximalneho poctu importovanych poloziek
    if(i > cfg.MAX_ITEMS_TO_IMPORT):
        break #prerus ak sa dosiahol maximalny pocet

PL.plot_all(cfg.ALL_VARIABLES_IN_SINGLE_TREND) # vykresli grafy

#zatvorenie suboru
fp.close()

#koniec
print('-----------------------------------------')
print('(c) 2019 by VONSCH s.r.o.')
# keby sme chceli podrzat konzolu
#input('Press Enter to exit')

