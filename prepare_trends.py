# common functions for all formats

#system modules
import os

# project modules
import simatic_files as sf
import weintek_files as wf
import plot_trends as plot

#detekcia typu suboru
def OpenTrendFile(filename):
    name, ext = os.path.splitext(filename) #need to know the extension
    basename = os.path.basename(filename) # only the basename of the file, not full path
    resultOK = False
    if(ext == '.txt'): # Simatic Basic Panel TXT file
        resultOK = sf.OpenSimaticTXTFile(filename)
    elif(ext == '.dtl'): # Weintek binary DTL files
        resultOK = wf.OpenWeintekDtlFile(filename)
    else:
        print('Error: Unsupported file type ',ext)

    if(resultOK):
        plot.close_plot() # close plot first
        plot.plot_all(basename) # vykresli grafy

# makes short prefix from the directory name, 'log_GF4' to 'GF4'...
def AddTrendFile(filename):
    name, ext = os.path.splitext(filename)
    basename = os.path.basename(filename) # only the basename of the file, not full path

    if(ext == '.dtl'): # Weintek binary DTL files
        resultOK = wf.OpenWeintekDtlFile(filename)
    else:
        print('Only DTL files can be added!')
        resultOK = False

    if(resultOK):
        plot.close_plot() # closes old plot first
        print('Closing old plot and redrawing')
        plot.plot_all(basename)
