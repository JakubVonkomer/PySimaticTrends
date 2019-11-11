#globalne premenne
varNames = []
#timeStrings = {} #dictionary of arrays
dateTimes = {} #dictionary of arrays
varValues = {} #dictionary of arrays
#timeMS_ = {}

#zadefinuje polia a slovniky pre novy nazov premennej
def AddNewVarName(varName):
    varNames.append(varName)
    #timeStrings[varName] = []
    varValues[varName] = []
    #timeMS_[varName] = []
    dateTimes[varName] = []