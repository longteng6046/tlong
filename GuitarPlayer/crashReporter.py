#!/usr/bin/python
# ------------------------------------------------------------------------------
# Go through the directory of .log files, look for the ones that has exception
# (except component not found ones)
# ------------------------------------------------------------------------------


# imports
import os
import sys
import time

# Check command format


if len(sys.argv) != 2:
    print "Format: ./crashFinder.py DIR/TO/LOGS"
    exit()

# get all log filenames
tmp = os.popen('ls ' + sys.argv[1]).readlines()
print "Path: " + sys.argv[1]
if len(tmp) == 0:
    print "File not found."
    print "error"
    exit()

# change to the directory
os.chdir(sys.argv[1])

# process each logfile
numberFault = 0
for item in tmp:
    fileName = item.strip()
    ## print fileName

    # print fileName

    # look for exceptions
    cmd = "cat " + fileName + " | grep 'NORMALLY TERMINATED'"
    ## print cmd
    
    # get the result of finding "Normal termination"
    result = os.popen(cmd).readlines() 

    # process the ones that didn't terminate properly
    if len(result) != 1:
        # print "Innormal Terminated!"
        file = open(fileName)
        lines = file.readlines()

        # process each line to find exceptions
        for i in range (0, len(lines) - 1):
            if lines[i].find("exception") == -1:
                continue
            elif lines[i].find("exception.ComponentNotFound") != -1:
                numberFault += 1
                # print "ComponentNotFound"
                continue
            elif lines[i].find("exception.ComponentDisabled") != -1:
                numberFault += 1
                # print "ComponentDisabled"
                continue
            elif lines[i].find("[Thread-4] ERROR - Uncaught exception") != -1 \
                 and lines[i+1].find("java.lang.NumberFormatException") != -1:
                print fileName.strip()
                for j in range(i - 10, i):
                    if lines[j].find("EventID") != -1 or lines[j].find("Finding widget") != -1:
                        print lines[j]
                print lines[i]
                continue
            else:
                print fileName.strip()
                for j in range(i - 10, i):
                    if lines[j].find("EventID") != -1 or lines[j].find("Finding widget") != -1:
                        print lines[j]
                print lines[i]
                # print lines[i-1].strip()
                # print lines[i].strip()
                # print lines[i+1].strip()                
        file.close()
print "Number of Component fault: "
print numberFault
        # process each line to find exceptions
        # for line in lines:
            # if line.find("exception") == -1:
                # continue
            # elif line.find("exception.ComponentNotFound") != -1:
                # continue
            # elif line.find("exception.ComponentDisabled") != -1:
                # continue
            # else:
                # print fileName.strip()
                # print line.strip()
                
        # file.close()
