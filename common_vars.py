# common vars for plots

#globalne premenne
varNames = []
#timeStrings = {} #dictionary of arrays
dateTimes = {} #dictionary of arrays
varValues = {} #dictionary of arrays
#timeMS_ = {}

useMiddleEndianFor32bitVars = True

#zadefinuje polia a slovniky pre novy nazov premennej
def AddNewVarName(varName):
    varNames.append(varName)
    #timeStrings[varName] = []
    varValues[varName] = []
    #timeMS_[varName] = []
    dateTimes[varName] = []

# clear all vars, before new trend
def ClearVars():
    varNames.clear()
    dateTimes.clear()
    varValues.clear()

# use or do not use MiddleEndian for 32bit variables
def SetMiddleEndianUsage(bool):
    global useMiddleEndianFor32bitVars

    useMiddleEndianFor32bitVars = bool
