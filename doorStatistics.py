"""

Hans Koberg, 2015

Program to compute some (long term) statistics of the door logging.

Ideas:
    Numbers:
        percentage open, closed, error? average, median, max, min.
        Longest open, closed, error? average, median, max, min. average open/closed/error time.
        How long logging time
        How often does the door change state? average, median, max, min.
        Lonest log streak without errors, average, median, max, min.
        

    Graphs:
        percentage over life time,
        percentage over 24h accumulated.
        When of 24h accumulated does the door change state most often.
    
    
    



Methods:
Fill in error locations to smooth data? Run data for smooth and unsmooth.
To smooth graphs, use floating window method.

"""

"""
 This method will miss values that are not logged. NO.
 Need to know the first date to start computing from.
 Also need to check that the changed from state is the right changed into state
 to validate the range check.
 
 add the right end date and state at the next loop.
"""


import datetime

def read_data(file_name,old_data = False):
    log = []
    with open(file_name, 'r') as f:
        last_to_state = "None"
        for line in f:
            try:
                line = line.split()
                start_date = datetime.datetime.strptime(line[0]+line[1],"%Y-%m-%d%H:%M:%S")
                from_state = line[5]
                to_state = line[7]
                
                if from_state == last_to_state:
                    last_state = from_state
                else:
                    last_state = "None"
                    
                #Correct the previous entry with the new information just read.
                if log != []:
                    log[-1] = (log[-1][0],start_date,last_state)
                
                log.append((start_date,"end_date",to_state))
                
                last_to_state = to_state
            except:
                pass
    
    if not old_data:
        endTime = datetime.datetime.now()
        log[-1] = (log[-1][0],endTime,log[-1][2])
    else:
        log.pop()

    return log


if __name__ == "__main__":
    read_data("oldStates.txt")