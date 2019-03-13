import matplotlib.pyplot as plt
import numpy as np

#globalne premenne
varNames = []
timeStrings = {} #dictionary, nie array!
varValues = {} #dictionary, nie array!
timeMS_ = {}

# odstranenie uvodzoviek z celeho riadku, nepotrebujeme nikde
def remove_quotes(str):
    return str.replace('"', '')

# parsovanie celeho riadku, naplnenie poli
def parseline(line):
    global varNames
    line1 = remove_quotes(line)
    words = line1.split()

    #deklaracia jednotlivych poloziek
    timeString = ''
    varValue = 0
    timeMS = 0

    #[0] - VarName, [1]+[2] - TimeString, [3] - VarValue, [4] - Validity, [5] Time_ms
    # niekedy sa varName sklada z dvoch slov (ma medzeru)
    words_length = len(words) # pocet slov
    if(words_length == 6): #varName nema medzeru
        varName = words[0]
        timeString = words[1]+words[2]
        varValue = float(words[3])
        timeMS = float(words[5])
    elif(words_length == 7): #varName ma medzeru
        varName = words[0]+'_'+words[1]
        timeString = words[2]+words[3]
        varValue = float(words[4])
        timeMS = float(words[6])
    else: #necakany pocet ???
        print('Assert failed: length of words is '+str(words_length))
        print(words)

    #test ci uz sme mali dany tag   
    if(varName not in varNames): # zadefinovanie poli pre dany key v dictionary
        varNames.append(varName)
        timeStrings[varName] = []
        varValues[varName] = []
        timeMS_[varName] = []

    # pridanie jednotlivych poloziek do pola/dictionary
    timeStrings[varName].append(timeString)
    varValues[varName].append(varValue)
    timeMS_[varName].append(timeMS)

# vykreslenie vsetkych grafov
def plot_all():
    i = 1 # trend number
    for varName1 in varNames:
        fig = plt.figure(i)  # an empty figure with no axes
        plt.suptitle('Trend of '+varName1)  # Add a title so we know which it is
        plt.plot(varValues[varName1])
        plt.xlabel('samples')
        plt.ylabel('Value of '+varName1)
        fig.show() #umozni vykreslit trendy paralelne, plt.show() by vykreslilo druhy az po zavreti prveho
        print('Drawing trend '+str(i)+': '+varName1)
        i+=1       

        
	
