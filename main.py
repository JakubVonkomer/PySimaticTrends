# main file, launcher of the app

import version as vs
import simatic_files as sf
import weintek_files as wf
import gui

print (vs.appTitle)

app = gui.AppGUI()
app.run()

# clean files
flesToDelete = ['config.py', 'parseline.py', 'file_dialog.py']

print(vs.appCopyrightInfo)
# keby sme chceli podrzat konzolu
#input('Press Enter to exit')
