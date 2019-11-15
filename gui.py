# gui and config processing

# gui
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# configparser
from configparser import ConfigParser

# project files
import version as vs
import prepare_trends as ppt
import tag_names
import common_vars

class AppGUI:

    # languages
    languageChoices = ["English","Polski"] #,"Русский"
    languageCodes = ["EN","PL"]

    paddingNSWE = 20 # default padding on all sides

    configSettings = {
        'configIniFile' : 'appconfig.ini',
        'defaultSection': 'default',
        'langDefault' : 'EN', # default language is English
        'useMiddleEndianDefault' : True, # default is True
    }
    
    # fills variables with proper texts
    def LoadTexts(self):
        # button texts

        lang = self.GetIniParam('lang') # get language
        if(lang == 'PL'):
            self.text_openButton = "Otwórz plik"
            self.text_addButton = "Dodaj plik do istniejącego trendu"
    
            #settings texts
            self.text_settings = "Ustawienia:"

            self.text_swapWords32bitVars = "Użyj Middle-endian dla zmiennych 32-bitowych"
            self.text_language = "Język:"
        else:
            # button texts
            self.text_openButton = "Open file"
            self.text_addButton = "Add file to existing trend"
    
            #settings texts
            self.text_settings = "Settings:"

            self.text_swapWords32bitVars = "Use Middle-endian for 32-bit variables"
            self.text_language = "Language:"

    # vymeni texty
    def ChangeTexts(self):
        self.openButton['text'] = self.text_openButton
        self.addButton['text'] = self.text_addButton
        self.labelSettings['text'] = self.text_settings
        self.useMiddleEndianCheckBox['text'] = self.text_swapWords32bitVars
        self.langLabel['text'] = self.text_language
        self.copyrightInfoLabel['text'] = vs.appCopyrightInfo

    # constructor, draws the window
    def __init__(self, master=None): 
    
        # creating basic window
        self.window = tk.Tk()
        #self.window.geometry("312x324") # size of the window width:- 500, height:- 375
        self.window.resizable(0, 0) # this prevents from resizing the window
        self.window.title(vs.appTitle)
        self.window.iconbitmap("images/vonsch.ico") # ikona

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # create the application
        print("Starting GUI...")

        # load configuration
        self.LoadIni()

        # load texts
        self.LoadTexts()

        # loads dictionary of tag names
        tag_names.LoadTagNames(self.GetIniParam('lang'))

        # buttony
        self.openButton = tk.Button(self.window, text = self.text_openButton, command=self.openButton_click, fg = "black")
        self.openButton.grid(row=0, column=0, padx=self.paddingNSWE, pady=self.paddingNSWE, sticky=tk.E+tk.N)# 'fg - foreground' is used to color the contents
        self.addButton = tk.Button(self.window, text = self.text_addButton, command=self.addButton_click, fg = "red", state=tk.DISABLED)
        self.addButton.grid(row=0, column=1, padx=self.paddingNSWE, pady=self.paddingNSWE, sticky=tk.W+tk.N) # 'text' is used to write the text on the Button

        ## settings
        self.labelSettings = tk.Label(self.window,text=self.text_settings)
        self.labelSettings.grid(row=2, column=0, columnspan=2, padx=self.paddingNSWE, pady=self.paddingNSWE, sticky=tk.W+tk.N)

        # use Middle-Endian (Weintek block read)
        self.useMiddleEndianCheckBox = tk.Checkbutton(self.window, text=self.text_swapWords32bitVars, variable=self.useMiddleEndianIntVar) # default je ON
        self.useMiddleEndianCheckBox.grid(row=4,column=0,columnspan=2)

        # language label
        self.langLabel = tk.Label(self.window,text=self.text_language)
        self.langLabel.grid(row=3, column=0) # , padx=self.paddingNSWE, pady=self.paddingNSWE, sticky=tk.E+tk.N

        # language combo box
        lang = self.GetIniParam('lang')
        langIndex = self.languageCodes.index(lang) #nacitanie indexu

        self.languageComboBox=ttk.Combobox(self.window,values=self.languageChoices,width=20)
        self.languageComboBox.grid(row=3,column=1,padx=self.paddingNSWE,pady=self.paddingNSWE,sticky=tk.E+tk.N)
        self.languageComboBox.current(langIndex)
        self.languageComboBox.bind('<<ComboboxSelected>>', self.languageComboBox_change)
        
        # copyright info
        self.copyrightInfoLabel = tk.Label(self.window, text=vs.appCopyrightInfo)
        self.copyrightInfoLabel.grid(row=5,column=0,columnspan=2,pady=self.paddingNSWE,sticky=tk.S)

    # kliknutie na openButton
    def openButton_click(self):
        common_vars.ClearVars() # erases all data before opening new file
        self.UpdateUseMiddleEndianVars() # updates the variable
        filename = self.OpenFileDialogGetFileName() # open dialog
        ppt.OpenTrendFile(filename) #opens file
        

    # kliknutie na addButton
    def addButton_click(self):
        pass # ToDo

    # zmena jazyka
    def languageComboBox_change(self, event=None):
        
        #tk.messagebox.showinfo("Info","Zmenil si jazyk!")
        langIndex = self.languageComboBox.current()
        lang = self.languageCodes[langIndex]
        self.configObj.set(self.configSettings['defaultSection'], 'lang', lang)
        
        # load and change the texts
        self.LoadTexts()
        self.ChangeTexts()

        # loads dictionary of tag names
        tag_names.LoadTagNames(lang) 

        # debug info to console
        if event: # <-- this works only with bind because `command=` doesn't send event
            print("Language changed to:", event.widget.get())

    # otvori dialog a vrati nazov suboru
    def OpenFileDialogGetFileName(self):
        file_path = filedialog.askopenfilename() # samoteny dialog
        return file_path

    # beh programu
    def run(self):
        self.window.mainloop()

    # Load ini file
    def LoadIni(self):

        self.configObj= ConfigParser()
        self.configObj.read(self.configSettings['configIniFile'])

        section = self.configSettings['defaultSection']
        
        # when ini file is empty or sections do not exist
        if section not in self.configObj:
            self.configObj.add_section(section)
            self.configObj.set(section,'lang', self.configSettings['langDefault'])
            self.configObj.set(section,'useMiddleEndian', str(self.configSettings['useMiddleEndianDefault']))
            useMiddleEndianLocal = True # default ON
        else: # ini file looks OK
            useMiddleEndianLocal = (self.configObj.getboolean(section, 'useMiddleEndian'))

        # naplnime useMiddleEndian, pouziva sa neskor pri inicializacii checkbuttonu
        self.useMiddleEndianIntVar = tk.IntVar(value=int(useMiddleEndianLocal))
        self.UpdateUseMiddleEndianVars()
        
    # update global variable
    def UpdateUseMiddleEndianVars(self):
        common_vars.SetMiddleEndianUsage(bool(self.useMiddleEndianIntVar.get())) # setting the global variable

    # save ini file
    def SaveIni(self):

        # deal with useMiddleEndian, different formats
        section = self.configSettings['defaultSection']
        useMiddleEndianBool = bool(self.useMiddleEndianIntVar.get())
        self.configObj.set(section,'useMiddleEndian', str(useMiddleEndianBool)) # double type conversion, wants boolean in form of string
        
        # write all configuration to file
        with open(self.configSettings['configIniFile'], 'w') as output_file:
            self.configObj.write(output_file)

    # reads ini parameter
    def GetIniParam(self, paramName, section = None):
        if(section == None):
            section = self.configSettings['defaultSection']

        return self.configObj[section][paramName]

    # when closing the window
    def on_closing(self):
        # save ini
        self.SaveIni()
        print('')
        print('Closing application...')
        self.window.destroy()
