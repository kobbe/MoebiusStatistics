# -*- coding: utf-8 -*-




import re
import datetime
import time
import numpy as np
# Change backend before importing pyplot in order
# to run the script without a running X server.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as dat
import matplotlib.dates as mdates

def parse(path='values.txt'):
    reg = re.compile('^[0-9]{14}(o|c|e)$')
    localLog = []
    start = time.time()
    count = 0
    f = open(path, 'r')
    match = reg.match
    append = localLog.append
    for line in f:
        if match(line) != None:
            #LIST.append((line[20:],datetime.datetime(int(line[0:4]), int(line[5:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19]))))
            #append((line[15:16],line[0:14]))
            append((line[14:15],datetime.datetime(int(line[0:4]),int(line[4:6]),int(line[6:8]),int(line[8:10]),int(line[10:12]),int(line[12:14]))))
            count += 1
            #if count % (1440*10) == 0:
            #    print (count)
        else:
            print("failed to match line %i which was: %s" % (count,line))
    f.close()
    end = time.time()
    print("it took %f seconds" % (end-start))
    return localLog
    #Also compute how many failed..

    
if __name__ == "__main__":
    LOG = parse('valuesFull.txt')
    
    last = LOG[-1][1]
    last = last.replace(minute=0,second=0,microsecond=0)
    first = LOG[0][1]
    first = first.replace(minute=0,second=0,microsecond=0)
    numHours = int((last-first).total_seconds()) // (60*60) #Convert to hwo many horus it is
    print (last,first,last-first,numHours)
    dateList = [[None,last - i*datetime.timedelta(hours=1)] for i in range(numHours ,-1,-1)]
    
    print(dateList[0]," to ",dateList[-1])
    
    #The last value have preccedence, if two
    #print(dateList[0]," to ",dateList[-1])
    
    #print(dateList[0],dateList[1],dateList[2],dateList[3],dateList[4])
    #print(dateList[-1],dateList[-2],dateList[-3],dateList[-4],dateList[-5])
    
    #Try to get the % of open for the last week for every hour. Need to know if Iammissing any values too. Get interval?
    #10080 values per 7 days.
    #Find first value >=datelist, step until
    stateListLow = []
    stateListHigh = []
    stateListLowNoFan = []
    stateListHighNoFan = []
    tempStart = 0
    for (_,date) in dateList:
        print(date)
        open = 0
        closed = 0
        openNoFan = 0
        closedNoFan = 0
        for i in range(tempStart,len(LOG)):
            #print(LOG[i][1], date)
            if LOG[i][1] < date - datetime.timedelta(days=7):
                tempStart = i
            elif LOG[i][1] >= date - datetime.timedelta(days=7) and LOG[i][1] <= date:
                if LOG[i][0] == 'o':
                    open +=1
                if LOG[i][0] == 'c':
                    closed+=1
                #if LOG[i][0] == 'o' and (LOG[i][1].weekday in [5, 6] or LOG[i][1].hour >=18 or LOG[i][1].hour <=7):
                #    openNoFan +=1
                #if LOG[i][0] == 'c' and (LOG[i][1].weekday in [5, 6] or LOG[i][1].hour >=18 or LOG[i][1].hour <=7):
                #    closedNoFan+=1
            else:
                break
        stateListLow.append(int((open/10080)*100))
        stateListHigh.append( ( (10080-closed)/10080) *100)
        #stateListLowNoFan.append(int((openNoFan/7080)*100))
        #stateListHighNoFan.append( ( (7080-closedNoFan)/7080) *100)
    
    #Fläkt av 14h per dag + 10 h lördag + 10 söndag
    
    #print(stateList)
    
    #print(dateList)
    x = [i[1] for i in dateList]
    #y = [i[0] for i in dateList]
    #x2 = [stateListLow]
    
    #print(stateListLow)
    #print(len(stateListLow),len(y),len(x))
    #print(x)
    
    fig, ax = plt.subplots()
    fig.autofmt_xdate()

    plt.xlabel('Datum')
    plt.ylabel('Bq/m$^{3}$')
    plt.title(u'RadonmÃ¤tvÃ¤rden frÃ¥n Moebius kÃ¤llare\n(Genererad: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ")")

    plt.gcf().subplots_adjust(bottom=0.25)
    #ax.plot_date(x,y,'-',marker='o')
    ax.plot_date(x,stateListLow,'-')
    ax.plot_date(x,stateListHigh,'-')
    #ax.plot_date(x,stateListLowNoFan,'-')
    #ax.plot_date(x,stateListHighNoFan,'-')
    
    ax.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d %H:00:00') )

    # Don't truncate the axes.
    if len(x) > 0:
        plt.xlim(x[0],x[-1])
    plt.ylim(ymin=0)

    plt.savefig("weekAverage2.png")
    