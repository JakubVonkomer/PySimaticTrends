import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import numpy as np

#globalne premenne
varNames = []
timeStrings = {} #dictionary of arrays
varValues = {} #dictionary of arrays
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

# ziska farbu grafu
def getPlotColor(trendNumber):
    colors = ['r','g','b','c','m','k','lime','tab:brown','sienna','teal','y']
    countOfColors = len(colors)
    return colors[trendNumber % countOfColors]

#globalne premenne, pouzivane viacerymi funkciami
trendsSubplots = [] # v tomto poli budu jednotlive subploty
labels = [] # v tomto poli budu jednotlive labely

# zaskrtavanie poloziek    
def ControlCheckFunc(label):
    index = labels.index(label)
    trendsSubplots[index].set_visible(not trendsSubplots[index].get_visible())
    plt.draw()


# vykreslenie vsetkych grafov
def plot_all(singleTrend=True):
    global trendsSubplots, labels # modifikujeme globalne premenne, vyuziva ich ControlCheckFunc
    trend_number = 1
    if(singleTrend): # jeden spolocny graf
 
        fig, ax = plt.subplots() # ani za svet neviem preco fig treba, ale bez toho mam AttributeError: 'tuple' object has no attribute 'plot'
        trendNumber = 0

        for varName1 in varNames:
            # timeStrings[varName1]
            plotTmp, = ax.plot(varValues[varName1], visible=True, lw=2, color=getPlotColor(trendNumber), label=varName1)
            trendsSubplots.append(plotTmp)
            trendNumber += 1
            print('Drawing subtrend '+str(trendNumber)+': '+varName1)
            #break

        plt.subplots_adjust(left=0.2)
        plt.suptitle('Trends')
        plt.xlabel('samples')
        plt.ylabel('Values')
 
        # Make checkbuttons with all plotted lines with correct visibility
        rax = plt.axes([0.01, 0.3, 0.15, 0.3])
        labels = [str(line.get_label()) for line in trendsSubplots]
        visibility = [line.get_visible() for line in trendsSubplots]
        check = CheckButtons(rax, labels, visibility)
        check.on_clicked(ControlCheckFunc)
        #maximalizacia grafu na cele okno
        # pouzivam rady z https://stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed') #works fine on Windows!
        #mng.frame.Maximize(True)
        plt.show()
    else: # viac grafov
        trendNumber = 0
        for varName1 in varNames:
            fig = plt.figure(trendNumber)  # an empty figure with no axes
            plt.suptitle('Trend of '+varName1)  # Add a title so we know which it is
            plt.plot(varValues[varName1])
            plt.xlabel('samples')
            plt.ylabel('Value of '+varName1)
            fig.show() #umozni vykreslit trendy paralelne, plt.show() by vykreslilo druhy az po zavreti prveho
            trendNumber+=1
            print('Drawing trend '+str(trendNumber)+': '+varName1)
            # sprava do konzoly a pocitadlo
         

        
	
