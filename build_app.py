# short app for building standalone application using pyinstaller

import subprocess
import os
import version as vs

targetFilename = vs.appTitle.replace('.','_')+'.exe'

pathToPyinstaller = "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pyinstaller.exe"
args = [pathToPyinstaller,'--onefile', '--add-data=images\\vonsch.ico;images' ,'main.py']

print('Building the app...')
proc = subprocess.run(args,shell=True, check=True)
print(proc)


print('Renaming to ',targetFilename)
os.rename('dist/main.exe','dist/'+targetFilename)



