# drawing plots using matplotlib

# libraries
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import matplotlib.dates as mdates

# project files
import tag_names as tn
from common_vars import *

# ziska farbu grafu
def getPlotColor(trendNumber):
    colors = ['r','g','b','c','m','k','lime','tab:brown','grey','teal','y']
    countOfColors = len(colors)
    return colors[trendNumber % countOfColors]

#globalne premenne, pouzivane viacerymi funkciami
trendsSubplots = [] # v tomto poli budu jednotlive subploty
labels = [] # v tomto poli budu jednotlive labely

# calculate yLim, manual autoscale for CheckButtons
def CalcYLim():
    yMin = 0 #min
    yMax = 0 #max
    for line in trendsSubplots:
        if(line.get_visible()):
            yMin = min(yMin,min(line.get_ydata()))
            yMax = max(yMax,max(line.get_ydata()))

    if(yMin == yMax):
        if(yMin == 0):
            yMax = yMin+1 # zeros, let's make it to <0,1>
        else:
            yMax = max(yMin * 1.01,) # different values, relative might be better if not zero

    relScaleExpandUpDown = 0.02 * (yMax-yMin) # 2% of the range bottom and up

    return (yMin-relScaleExpandUpDown) ,(yMax+relScaleExpandUpDown)

# zaskrtavanie poloziek    
def ControlCheckFunc(label):
    index = labels.index(label)
    trendsSubplots[index].set_visible(not trendsSubplots[index].get_visible())
    # recompute the ax.dataLim
    #ax.relim()
    # update ax.viewLim using the new dataLim
    #ax.autoscale_view()
    
    #plt.autoscale(enable=True, axis='both')
    yMin,yMax = CalcYLim()
    ax.set_ylim(bottom=yMin,top=yMax) # sets new Y limits
    plt.draw()

# clears plot globals, before new trend is drawn
def ClearPlotGlobals():
    global trendsSubplots, labels
    trendsSubplots.clear()
    labels.clear()

# zmena nazvu tagu, mozne premenovanie alebo preklad nazvu tagu
def TranslateTagName(tagName1):
    if tagName1 in tn.tagNames:
        return tn.tagNames[tagName1]
    else:
        return tagName1

# vykreslenie vsetkych grafov
def plot_all(singleTrend=True):
    global trendsSubplots, labels, ax, fig # modifikujeme globalne premenne, vyuziva ich ControlCheckFunc

    ClearPlotGlobals() # vymaze stare data

    trend_number = 1
    if(singleTrend): # jeden spolocny graf
 
        fig, ax = plt.subplots() # fig treba lebo subplots vracia tuple
        trendNumber = 0

        print('') # empty line
        print('Drawing new trend')

        for varName1 in varNames:
            # vracia tuple, preto ciarka za plotTmp
            plotTmp, = ax.step(dateTimes[varName1],varValues[varName1], visible=True, lw=2, color=getPlotColor(trendNumber), label=TranslateTagName(varName1))
            trendsSubplots.append(plotTmp)
            trendNumber += 1
            print('Drawing subtrend '+str(trendNumber)+': '+varName1 + ' alias ' + TranslateTagName(varName1))
            #break

        plt.subplots_adjust(left=0.28) #odkade nalavo zacina graf, treba nechat offset na legendu
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
        legendHeight = 0.015 * len(varNames) + 0.05 # height legend, estimation
        rax = plt.axes([0.01, 0.3, 0.20, legendHeight]) # legenda offset zlava, zdola, sirka, vyska
        labels = [str(line.get_label()) for line in trendsSubplots]
        visibility = [line.get_visible() for line in trendsSubplots]
        check = CheckButtons(rax, labels, visibility)
        check.on_clicked(ControlCheckFunc)

        # ofarbenie grafov, index labelov sedi s indexom varName1-ov
        for label1 in labels:
            i = labels.index(label1)
            check.labels[i].set_color(getPlotColor(i))
            check.labels[i].set_fontsize(8)
            x,y = check.labels[i].get_position()
            x_new = x - 0.1 # posun dolava
            if(x_new <= 0):
                x_new = 0.01
            check.labels[i].set_x(x_new)
        
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
            plt.step(dateTimes[varName1], varValues[varName1])
            plt.xlabel('Time')
            plt.ylabel('Value of '+varName1)
            _=plt.xticks(rotation=45)   
            fig.show() #umozni vykreslit trendy paralelne, plt.show() by vykreslilo druhy az po zavreti prveho
            trendNumber+=1
            print('Drawing trend '+str(trendNumber)+': '+varName1)
            # sprava do konzoly a pocitadlo
