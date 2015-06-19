#!/usr/bin/python -u
# -*- coding:utf-8 -*-

import datetime
import time
from pylab import *
from functools import reduce

LIST = []

#TODO:
#Should be able to change start and end dates while running.
#vardag, helg, 
#skillnad måndaer, dagar etc



#Should fill in the gaps?

#line 224 356 is corrupted..

def parse(path='values.txt'):
    start = time.time()
    count = 0
    f = open(path, 'r')
    for line in f:
        if len(line) > 5:
            #LIST.append((line[20:],datetime.datetime(int(line[0:4]), int(line[5:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19]))))
            LIST.append((line[20:21]=='o',line[0:19]))
        count = count+1
        if count % (1440*10) == 0:
            print count
    end = time.time()
    print "time taken", end - start,"s"
    f.close()

#LIST.append((line[20:],time.strptime(line[0:19],"%Y %m %d %H %M %S")))

#LIST.append((line[20:],datetime.datetime(line[0:4], line[5:7], line[8:10], line[11:13], line[14:16], line[17:19])))

#LIST.append((line[20:],line[0:19]))

def printStats():

    print u"Antal datapunkter är:", len(LIST)
    print u"Eller", len(LIST)/60/24 , u"dagar av loggning"
    nropen = reduce((lambda x, (a,b): x+a),LIST,0)
    print u"Öppen% är:" + str( nropen/float(len(LIST)))

    longest = 0
    temp = 0
    for i in LIST:
        (a,b) = i
        if a==True:
            temp = temp + 1
        else:
            if temp > longest:
                longest=temp
            temp=0
    if temp > longest:
        logest=temp

    

    print u'Längsta loggade öppet i stäck (kan vara icke kontinuerligt) är:', longest, "minuter"
    print u'eller:', longest/60, u'timmar, eller:', longest/60/float(24)

    longest = 0
    temp = 0
    for i in LIST:
        (a,b) = i
        if a==False:
            temp = temp + 1
        else:
            if temp > longest:
                longest=temp
            temp=0
    if temp > longest:
        logest=temp

    

    print u'Längsta loggade stängt i stäck (kan vara icke kontinuerligt) är:', longest, "minuter"
    print u'eller:', longest/60, u'timmar, eller:', longest/60/float(24)

    

    longest = 0
    temp = 0
    oldDate = datetime.datetime(int(LIST[0][1][0:4]), int(LIST[0][1][5:7]), int(LIST[0][1][8:10]), int(LIST[0][1][11:13]), int(LIST[0][1][14:16]), int(LIST[0][1][17:19]))
    for i in LIST:
        (a,b) = i
        newDate = datetime.datetime(int(b[0:4]), int(b[5:7]), int(b[8:10]), int(b[11:13]), int(b[14:16]), int(b[17:19]))
        if a==True and (newDate-oldDate).total_seconds() < 90:
            temp = temp + 1
        else:
            if temp > longest:
                longest=temp
            temp=0
        oldDate = newDate
    if temp > longest:
        logest=temp

    print u'Längsta loggade kontinuerligt är:', longest, "minuter"
    print u'eller:', longest/60, u'timmar, eller:', longest/60/float(24)

    longest = 0
    temp = 0
    oldDate = datetime.datetime(int(LIST[0][1][0:4]), int(LIST[0][1][5:7]), int(LIST[0][1][8:10]), int(LIST[0][1][11:13]), int(LIST[0][1][14:16]), int(LIST[0][1][17:19]))
    for i in LIST:
        (a,b) = i
        newDate = datetime.datetime(int(b[0:4]), int(b[5:7]), int(b[8:10]), int(b[11:13]), int(b[14:16]), int(b[17:19]))
        if a==False and (newDate-oldDate).total_seconds() < 90:
            temp = temp + 1
        else:
            if temp > longest:
                longest=temp
            temp=0
        oldDate = newDate
    if temp > longest:
        logest=temp

    print u'Längsta loggade kontinuerligt är:', longest, "minuter"
    print u'eller:', longest/60, u'timmar, eller:', longest/60/float(24)

def distrubutionOverDay():
    y = [0]*(24*60)
    for i in LIST:
        (a,b) = i
        index = int(b[11:13])*60+int(b[14:16])
        y[index] = y[index] + 1

    


    

    print u"Max:", max(y)
    print u"Min:", min(y)
    print u"Medel:", sum(y)/float(len(y))

    #Test to sort 2min on either side and upwards untill middle..
    y2 = sort(y)
    y2 = y2.tolist()
    y3 = y2[len(y2)%2::2] + y2[::-2]
    x = range(0,24*60)
    title(u'Distrubutionen av datapunkter över dagen')
    plot(x,y)
    show()
    title(u'Distrubutionen av datapunkter över dagen, sorterad')
    plot(x,y2)
    show()
    title(u'Distrubutionen av datapunkter över dagen, sorterad som normaldistrubution')
    plot(x,y3)
    show()
    

def distrubutionOpenOverDay():
    nrTotal = [0]*(24*60)
    nrOpen = [0]*(24*60)
    for i in LIST:
        (a,b) = i
        index = int(b[11:13])*60+int(b[14:16])
        nrTotal[index] = nrTotal[index] + 1
        if a==True:
            nrOpen[index] = nrOpen[index] + 1
    x = range(0,24*60)
    probOpen = [float(ai)/bi for ai,bi in zip(nrOpen,nrTotal)]
    title(u'Hur ofta det är öppet på dygnet')
    plot(x,probOpen)
    show()
    
        
def plot2():
    x = range(0,len(LIST))
    y = [a for (a,b) in LIST]

    #plot(x,y) 'one curve'
    #fill(x,y) 'just bad'
    #fill_between(x,y,y2=0,color='r')
    #stackplot(x,y) same as fill_between
    show()

    
parse()
printStats()

#distrubutionOverDay()
#distrubutionOpenOverDay()

#Ideas
"""
*Sort graphs from 0 to fully open.
*all on a single graphs, sort it too..
*Per minute of day
*% open per day
"""
    
