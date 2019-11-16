# support for weintek panel .dtl logs
import struct # podpora binarnych struktur
#import sys
from datetime import datetime # datumove funkcie

import common_vars

## globalne premenne`
nrVars = 0 # pocet premennych

formatStructRead = '' # format struktury na citanie v pythone, bude stavany priebezne
formatStructType = '' # format struktury vyznamu dat, bude stavany priebezne

# konstanty
typ32bitMiddleEndian = 'L'

DTL_TYPES = {
#     nazov, skutocny typ, nahradzovany typ pre lahsie spracovanie dat
0: ('16-bit BCD', 'H', 'H'),
1: ('32-bit BCD', 'L', typ32bitMiddleEndian),
2: ('16-bit Unsigned', 'H', 'H'),
3: ('16-bit Signed', 'h' , 'h'),
4: ('32-bit Unsigned', 'L', typ32bitMiddleEndian),
5: ('32-bit Signed', 'l', typ32bitMiddleEndian),
6: ('32-bit Float', 'f', typ32bitMiddleEndian),
7: ('String', 's','s')
}

# preinterpretuje Int ako Float, bitovy vyznam
def reinterpretAsFloat(integer):
    return struct.unpack('!f', struct.pack('!I', integer))[0]

# vymeni 2 bajty v 32bitovom Inte
def swapWordsInt32(integer):
    bits0to15 = integer & 0x0000FFFF
    bits16to31 = (integer & 0xFFFF0000) >> 16
    return (bits0to15 << 16) | bits16to31

# spracovanie spravnych dat
def ProcessDTLValue(datastruct, index):

    item1 = datastruct[index]
    #print('datastruct[',index,'] = ',datastruct[index],'Format=',formatStructType[index])

    fsIndex = index # timestamp a ms su prve polozky struktury, prve data su na indexe 2

    # multiple variable files can be middle endian only
    if(nrVars > 1 and common_vars.useMiddleEndianFor32bitVars):
        if(formatStructType[fsIndex] == 'f' or formatStructType[fsIndex] == 'L' or formatStructType[fsIndex] == 'l'): # ak je to float, alebo (u)int32
            item1 = swapWordsInt32(item1)
            
    # recast as float
    if(formatStructType[fsIndex] == 'f'):
        item1 = reinterpretAsFloat(item1)
                    
    return item1


# nacitanie DTL suboru z panelu weintek
def OpenWeintekDtlFile(filename):

    global formatStructType, formatStructRead, nrVars # tieto globalne premenne sa tu modifikuju

    #Otvorenie suboru
    try:
        fp = open(filename, "rb") #treba dat to utf-16, inak masaker

    # obsluha chyby
    #except FileNotFoundError:
    except Exception as e:
        print(e)
        return False

    # binarne citanie suboru

    fp.seek(0,0) # chod na poziciu 8+4

    fileType = fp.read(7) # typ suboru

    #print('FileType = ',fileType)
    # b'_dtl\x00 \x01'
    # b'\x5f\x64\x74\x63\x00\x20\x01'
    if(fileType != b'_dtl\x00 \x01'):
        print('Unknown file format') # chybove hlasenie
        return False

    fp.seek(12,0) # chod na poziciu 8+4

    # nacitanie informacie o velkosti struktury a dat
    headerInfo = struct.unpack('<LL' , fp.read(8)) # [0] pocet premennych, [1] - pocet dat
    nrVars =  headerInfo[0]
    print('Number of variables: ', nrVars , ' Struct length (no time): ',headerInfo[1])

    formatStructRead = '<Lb' # format struktury na citanie v pythone, bude stavany priebezne
    formatStructType = 'Lb' # format struktury vyznamu dat, bude stavany priebezne
    # rozdiel je v 32bitovych datach kde nemusi sediet endianess

    # nacitanie informacie o jednotlivych polozkach struktury
    for i in range(0,nrVars):
        varType = struct.unpack('<LL' , fp.read(8)) # typ premennej, 6 je float, 4 unsigned int
        #print('Typ premennej ', varType, ': ', DTL_TYPES[varType[0]][0],'Word length: ',varType[1])   
        formatStructRead += DTL_TYPES[varType[0]][2] # typ ktory sa cita zo suboru
        formatStructType += DTL_TYPES[varType[0]][1] # skutocny vyznam dat

    #print('Format Read: ',formatStructRead)
    #print('Format Type: ',formatStructType)
    formatLength = struct.calcsize(formatStructRead)
    #print('FormatLength: ', formatLength)

    # kontrola stringu 'name'    
    nameCheck = struct.unpack('<4s' ,  fp.read(4))
    #print('name = ',nameCheck)

    # zobratie nazvov
    for i in range(0,headerInfo[0]):
        nameLength = struct.unpack('<H' ,  fp.read(2))
        nameRawData = fp.read(nameLength[0])
        name = nameRawData.decode('utf-8')
        # pridaj zaznam a vytvor polia
        common_vars.AddNewVarName(name)
        #print('Length: ',nameLength[0], 'Name: ',name)

    # nacitanie samotnych dat

    dataSize = struct.calcsize(formatStructRead)
    structsReadCounter = 0 # pocitadlo nacitanych struktur
    while(True):
        buffer = fp.read(dataSize)
                
        # detekcia konca suboru
        if(len(buffer) < dataSize):
            if(len(buffer) > 0):
                print("Warning: possibly corupted data.")
            break
        
        structsReadCounter += 1 # inkrement struktur

        # struktura nacitana OK, spracuvame data
        data = struct.unpack(formatStructRead , buffer) # [0] pocet premennych, [1] - pocet dat

        # zoberieme cas
        timestamp = datetime.utcfromtimestamp(data[0]) # cas by sme mali
        
        # prejdenie jednotlivych dat v jednom riadku struktury
        for j in range(0,nrVars):
            actualName = common_vars.varNames[j] # prve dva stlpce su datetime a ms, preto posuvame #TU JE PROBLEM, FIXME
            common_vars.dateTimes[actualName].append(timestamp)
            value = ProcessDTLValue(data,j+2) #prve hodnoty v data strukture su od indexu 2
            common_vars.varValues[actualName].append(value)

    #zatvorenie suboru
    fp.close()
    
    # detekcia nenulovych dat
    if(structsReadCounter == 0):
        # ak nemame ziadne data, je zle
        return False

    # STOP here, debug only
    #x = 3 / 0

    # return
    return True

