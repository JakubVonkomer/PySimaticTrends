# common functions for all formats

#system modules
import os

# project modules
import simatic_files as sf
import weintek_files as wf
import plot_trends as plot

#detekcia typu
def OpenTrendFile(filename):
    name, ext = os.path.splitext(filename)
    resultOK = False
    if(ext == '.txt'): # Simatic Basic Panel TXT file
        resultOK = sf.OpenSimaticTXTFile(filename)
    elif(ext == '.dtl'): # Weintek binary DTL files
        resultOK = wf.OpenWeintekDtlFile(filename)
    else:
        print('Error: Unsupported file type ',ext)

    if(resultOK):
        plot.plot_all(True) # vykresli grafy

