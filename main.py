# main file, launcher of the app

import version as vs
import simatic_files as sf
import weintek_files as wf
import gui

import os

print (vs.appTitle)

app = gui.AppGUI()
app.run()

# clean unused files, for 3.0.0+
filesToDelete = ['config.py', 'parseline.py', 'file_dialog.py']

for file in filesToDelete:
    if(os.path.exists(file)):
        print('Deleting file ',file)
        os.remove(file)

print(vs.appCopyrightInfo)
# keby sme chceli podrzat konzolu
#input('Press Enter to exit')
