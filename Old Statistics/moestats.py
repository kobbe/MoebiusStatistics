#!/usr/bin/python -u
# -*- coding:utf-8 -*-

#use python3

#use one file that is a cumulative stats file.

#How long have it been open/closed.

#Graph over open/closed/error for day, week, month, year and total.

#Basic stats, for day, week, month, year and total.
    #Number of logg points
    #Logging since
    #Number of minutes not logged
    #Open/closed %
    
#Graph over prop of open for day,week,month,year and total.

#Run more advanced data not so often.

import re
import datetime

LOG = []
reg = re.compile('^[0-9]{14}(o|c|e)$')



def parse(path='values.txt'):
    localLog = []
    start = time.time()
    count = 0
    f = open(path, 'r')
    match = reg.match
    append = localLog.append
    for line in f:
        if match(line) != None:
            append((line[14:15],datetime.datetime(int(line[0:4]),int(line[4:6]),int(line[6:8]),int(line[8:10]),int(line[10:12]),int(line[12:14])),line[0:14]))
            count += 1
        else:
            print("failed to match line %i which was: %s" % (count,line))
    f.close()
    end = time.time()
    print("it took %f seconds" % (end-start))
    return localLog

LOG = parse("~/Dekstop/Python/values")

    