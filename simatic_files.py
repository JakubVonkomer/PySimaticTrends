import config as cfg
import re
import datetime
import numpy as np

from common_vars import *

# odstranenie uvodzoviek z celeho riadku, nepotrebujeme nikde
def remove_quotes(str):
    return str.replace('"', '')

# parsovanie datumu a casu
def datetimefromisoformat(strDateTime):
    #print('datetimefromisoformat: '+strDateTime) #debug
    dP = re.split(' |-|:',strDateTime)
    dateX = datetime.datetime(int(dP[0]),int(dP[1]),int(dP[2]),int(dP[3]),int(dP[4]),int(dP[5]))
    return dateX

# parsovanie celeho riadku, naplnenie poli
def parseline(line):
    global varNames
    line1 = remove_quotes(line)
    words = line1.split()

    #deklaracia jednotlivych poloziek
    timeString = ''
    varValue = 0
    timeMS = 0
    varName_delimiter = '_'

    #[0] - VarName, [1]+[2] - TimeString, [3] - VarValue, [4] - Validity, [5] Time_ms
    # niekedy sa varName sklada z dvoch slov (ma medzeru)
    words_length = len(words) # pocet slov
    if(words_length < 6):
        return # ingorujeme chybne a divne riadky
    else: #jedna a viac medzier vo VarName
        timeMS = float(words[words_length-1])
        varValue = float(words[words_length-3])
        timeString = words[words_length-5]+' '+words[words_length-4]
        varName = varName_delimiter.join(words[0:(words_length-5)])

    if(varName not in varNames): # zadefinovanie poli pre dany key v dictionary
        AddNewVarName(varName)

    #konvertovanie datumu
    dateTime1 = datetimefromisoformat(timeString)

    # pridanie jednotlivych poloziek do pola/dictionary
    #timeStrings[varName].append(timeString)
    varValues[varName].append(varValue)
    #timeMS_[varName].append(timeMS)
    dateTimes[varName].append(dateTime1)

# nacitanie simaticovskeho TXT suboru
def OpenSimaticTXTFile(filename):
    try:
        fp = open(filename, "r" ,encoding='utf-16') #treba dat to utf-16, inak masaker

    # obsluha chyby
    #except FileNotFoundError:
    except Exception as e:
        print(e)
        return false

    # parsing file    
    i = 0
    for line in fp:

        # kontrola na IGNORE_VARNAMES
        ignored_line = [line.find(ignoreVarname1) for ignoreVarname1 in cfg.IGNORE_VARNAMES]
        if(i > 0 and (not 1 in ignored_line)):
            parseline(line) # jadro
        i=i+1

        # kontrola maximalneho poctu importovanych poloziek
        if(i > cfg.MAX_ITEMS_TO_IMPORT):
            break #prerus ak sa dosiahol maximalny pocet

    fp.close() # ukoncenie suboru
    return true
