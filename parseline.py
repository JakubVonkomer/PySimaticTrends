import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import matplotlib.dates as mdates
import numpy as np
import re
import datetime

#globalne premenne
varNames = []
timeStrings = {} #dictionary of arrays
dateTimes = {} #dictionary of arrays
varValues = {} #dictionary of arrays
timeMS_ = {}

# odstranenie uvodzoviek z celeho riadku, nepotrebujeme nikde
def remove_quotes(str):
    return str.replace('"', '')

# parsovanie datumu a casu
def datetimefromisoformat(strDateTime):
    #print('datetimefromisoformat: '+strDateTime) #debug
    dP = re.split(' |-|:',strDateTime)
    dateX = datetime.datetime(int(dP[0]),int(dP[1]),int(dP[2]),int(dP[3]),int(dP[4]),int(dP[5]))
    return dateX

# parsovanie celeho riadku, naplnenie poli
def parseline(line):
    global varNames
    line1 = remove_quotes(line)
    words = line1.split()

    #deklaracia jednotlivych poloziek
    timeString = ''
    varValue = 0
    timeMS = 0
    varName_delimiter = '_'

    #[0] - VarName, [1]+[2] - TimeString, [3] - VarValue, [4] - Validity, [5] Time_ms
    # niekedy sa varName sklada z dvoch slov (ma medzeru)
    words_length = len(words) # pocet slov
    if(words_length == 6): #varName nema medzeru
        varName = words[0]
        timeString = words[1]+' '+words[2]
        varValue = float(words[3])
        timeMS = float(words[5])
    else: #vela medzier
        timeMS = float(words[words_length-1])
        varValue = float(words[words_length-3])
        timeString = words[words_length-5]+' '+words[words_length-4]
        varName = varName_delimiter.join(words[0:(words_length-5)])
        		
        #print('Assert failed: length of words is '+str(words_length))
        #print(words)

    #test ci uz sme mali dany tag   
    if(varName not in varNames): # zadefinovanie poli pre dany key v dictionary
        varNames.append(varName)
        timeStrings[varName] = []
        varValues[varName] = []
        timeMS_[varName] = []
        dateTimes[varName] = []

    #konvertovanie datumu
    dateTime1 = datetimefromisoformat(timeString)

    # pridanie jednotlivych poloziek do pola/dictionary
    timeStrings[varName].append(timeString)
    varValues[varName].append(varValue)
    timeMS_[varName].append(timeMS)
    dateTimes[varName].append(dateTime1)

# ziska farbu grafu
def getPlotColor(trendNumber):
    colors = ['r','g','b','c','m','k','lime','tab:brown','grey','teal','y']
    countOfColors = len(colors)
    return colors[trendNumber % countOfColors]

#globalne premenne, pouzivane viacerymi funkciami
trendsSubplots = [] # v tomto poli budu jednotlive subploty
labels = [] # v tomto poli budu jednotlive labely

# zaskrtavanie poloziek    
def ControlCheckFunc(label):
    index = labels.index(label)
    trendsSubplots[index].set_visible(not trendsSubplots[index].get_visible())
    # recompute the ax.dataLim
    #ax.relim()
    # update ax.viewLim using the new dataLim
    #ax.autoscale_view()
    plt.draw()


# vykreslenie vsetkych grafov
def plot_all(singleTrend=True):
    global trendsSubplots, labels # modifikujeme globalne premenne, vyuziva ich ControlCheckFunc
    #global ax,fig
    trend_number = 1
    if(singleTrend): # jeden spolocny graf
 
        fig, ax = plt.subplots() # ani za svet neviem preco fig treba, ale bez toho mam AttributeError: 'tuple' object has no attribute 'plot'
        trendNumber = 0

        for varName1 in varNames:
            # nie uplne chapem tej ciarke za plotTmp, ale musi byt
            plotTmp, = ax.plot(dateTimes[varName1],varValues[varName1], visible=True, lw=2, color=getPlotColor(trendNumber), label=varName1)
            trendsSubplots.append(plotTmp)
            trendNumber += 1
            print('Drawing subtrend '+str(trendNumber)+': '+varName1)
            #break

        plt.subplots_adjust(left=0.2)
        plt.suptitle('Trends')
        plt.xlabel('Time')
        plt.ylabel('Values')

        # Xova mierka pre cas
        #hours = mdates.MinuteLocator(15)   # every hour
        #mins = mdates.MinuteLocator(5)  # every minute
        #ax.xaxis.set_major_locator(hours)
        #ax.xaxis.set_minor_locator(mins)

        # hlavna mierka s datumom, mensia iba cas
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m %H:%M:%S"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M:%S"))
        
        _=plt.xticks(rotation=45)   
 
        # Make checkbuttons with all plotted lines with correct visibility
        rax = plt.axes([0.01, 0.3, 0.15, 0.3])
        labels = [str(line.get_label()) for line in trendsSubplots]
        visibility = [line.get_visible() for line in trendsSubplots]
        check = CheckButtons(rax, labels, visibility)
        check.on_clicked(ControlCheckFunc)

        # ofarbenie grafov, index labelov sedi s indexom varName1-ov
        for label1 in labels:
            i = labels.index(label1)
            check.labels[i].set_color(getPlotColor(i))
        
        #maximalizacia grafu na cele okno
        # pouzivam rady z https://stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed') #works fine on Windows!
        #mng.frame.Maximize(True)

        #grid
        ax.grid(b=True, which='both', color='#cccccc', linestyle='--')
        plt.show()
    else: # viac grafov
        trendNumber = 0
        for varName1 in varNames:
            fig = plt.figure(trendNumber)  # an empty figure with no axes
            plt.suptitle('Trend of '+varName1)  # Add a title so we know which it is
            plt.plot(dateTimes[varName1], varValues[varName1])
            plt.xlabel('Time')
            plt.ylabel('Value of '+varName1)
            _=plt.xticks(rotation=45)   
            fig.show() #umozni vykreslit trendy paralelne, plt.show() by vykreslilo druhy az po zavreti prveho
            trendNumber+=1
            print('Drawing trend '+str(trendNumber)+': '+varName1)
            # sprava do konzoly a pocitadlo
         

        
	
