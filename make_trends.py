import sys
#import os
import parseline as PL
import version as vs
import config as cfg

print (vs.appName + ' ' + vs.version)
print ('')

#print (sys.argv)

# argv[1] je nazov suboru na otvorenie
if len(sys.argv) > 1:
    filename = sys.argv[1]
elif(cfg.ASK_FOR_FILENAME):
    filename = input("Enter file name: ")
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
    if(i > 0):
        PL.parseline(line)
    i=i+1

    # kontrola maximalneho poctu importovanych poloziek
    if(i > cfg.MAX_ITEMS_TO_IMPORT):
        break #prerus

PL.plot_all() # vykresli

#zatvorenie suboru
fp.close()

#koniec
print('-----------------------------------------')
print('(c) 2019 by Jakub Vonkomer, VONSCH s.r.o.')
# keby sme chceli podrzat konzolu
#input('Press Enter to exit')

