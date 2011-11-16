#!/usr/bin/python
##############################
#
# File: lcovPlus.py
# Author: Teng Long (tlong@cs.umd.edu)
# Version: 0.3.2
# Descrpition:
#   This is a tool that provides enhanced features processing tracefiles(.info)
#   generated by lcov.
# Created: Jul. 25th, 2011
# Updated:
#   Jul 26, 2011: Changed the option processing with "getopt" module of python
#   Aug 22, 2011: Add the function of coverage frequency statistics
#   Aug 28, 2011: Add the function of coverage distribution statistics
#   Nov 16, 2011: Add coverage difference support. 
# Bugs:
#   1. if use with '| less' in Unix/Linux, a "Broken pipe" excpetion
#      will be raised.
#   2. when (-r rl r2), r1 and r2 should be anble to be quoted by ""
##############################


import os
import sys
import getopt

debugFlag = False

def printerr(content):
    if type(content) != type("string"):
        content = str(content)
    if debugFlag == True:
        sys.stderr.write(content + '\n')
        
def errorInfo():
    print >> sys.stderr, "Use lcovPlus --help to get more information"
    sys.exit(1)

def help():
    print '''Usage: lcovPlus [OPTIONS|OPERATIONS]

Use lcovPlus to process tracefile generated by lcov.

Misc:
  -h, --help                    Print this help, then exit
  -v, --version                 Print version Number, then exit

Operation:
  -a, --add-tracefile FILE      Add contents of tracefile
  -r, --replace                 Replace the prefix of source files
  -s, --stat-freq               Count the coverage frequency of functions
      --cov-dist                Coverage overlap distribution of multiple
                                  trace files
      --diff                    when add A.info and B.info, count coverage of
                                  parts that in A but not B
  Be careful: only one of '-r', '-s', '--cov-dist' and '--diff' operation
    can be used each time.
  
Options:
  -f file|function              Specify the output format of frequency
                                statistics. The default output is the frequency of
                                files hitted. This option will be skipped if not in
                                '-s' mode.
     --aggregate                If the output format is 'file', this option aggregates
                                files into directories.
  -o, --output-file FILENAME    Write data to FILENAME instead of stdout
  
  -d, --debug-mode              Output debug information for lcovPlus
  
To report a bug, please contact tlong@cs.umd.edu
'''    

## Get arguments
args = sys.argv[1:]
optlist, args = getopt.gnu_getopt(args, "hvrsf:da:o:", ['help', 'version', 'replace', 'add-tracefile', 'freq-stat', 'output-file', 'debug-mode', 'cov-dist', 'diff', 'aggregate']) # option list


##############################
# option & argument processing
##############################

aFlag = False
rFlag = False
oFlag = False
sFlag = False
dFlag = False
diffFlag = True
aggFlag = False

## singple options/operations

opts = [opt[0] for opt in optlist]

if '--help' in opts or '-h' in opts:
    help()
    sys.exit(0)

elif '--version' in opts or '-v' in opts:
    print version
    sys.exit(0)

if '-d' in opts or '--debug-mode' in opts:
    debugFlag = True

if '-s' in opts or '--stat-freq' in opts:
    sFlag = True
if '--cov-dist' in opts:
    dFlag = True
if '--diff' in opts:
    diffFlag = True
if '--aggregate' in opts:
    aggFlag = True

infileList = [] # the list of added inputed files.
replacePair = None # the list of prefix replacement pairs
outputFile = None


# multi-arg options/operations, some skiped options are parsed in sub
#  sections.
for item in optlist:
    if item[0] == '-a' or item[0] == '--add-tracefile':
        aFlag = True
        infileList.append(item[1])

    elif item[0] == '-r' or item[0] == '--replace':
        rFlag = True
        if len(args) == 2:
            replacePair = (args[0], args[1])
        else:
            errorInfo()
    elif item[0] == '-o' or item[0] == '--output-file':
        oFlag = True
        outputFile = item[1]
    # else:
        # errorInfo()
        
printerr("infileList: " + str(infileList))
printerr("replacePair: " + str(replacePair))


##############################
# flags checking
##############################
flagCountT = 0
if rFlag == True:
    flagCountT += 1
if sFlag == True:
    flagCountT += 1
if dFlag == True:
    flagCountT += 1
if diffFlag == True:
    flagCountT += 1

if flagCountT > 1:
    print >> sys.stderr, "lcovPlus: Please choose only one operation from -s, -r and --cov-dist"
    errorInfo()
elif flagCountT == 0:
    print >> sys.stderr, "lcovPlus: Please at least choose one operation from -s, -r or --cov-dist."
    errorInfo()
#################
# Output choice
#################
if oFlag == True: # output file specified
    outstream = open(outputFile, 'w')
else:
    outstream = sys.stdout



##############################
# dealing with '-r': replacement
##############################
if rFlag == True:
    if len(infileList) == 0:
        print >> sys.stderr, "lcovPlus: Please add exactly ONE tracefile by '-a' for replacement"
        errorInfo()
    elif len(infileList) >= 2:
        print >> sys.stderr, "lcovPlus: Please only add ONE tracefile for replacement"
        errorInfo()
    else:
            
        infile = open(infileList[0], 'r')
        for item in infile.readlines():
            if not item.startswith("SF:"):
                try:
                    outstream.write(item)
                except:
                    None
            else: # the 'SF:' lines
                rawline = item[3:]
                replaceFlag = False # whether replaced anything
                # compare every replacement pair
                if rawline.startswith(replacePair[0]):
                    newline = 'SF:' + replacePair[1] + rawline[len(replacePair[0]):]
                    replaceFlag = True
                if replaceFlag == False:
                    outstream.write(item)
                else:
                    outstream.write(newline)
                    

        # Close files
        infile.close()
        if oFlag == True:
            outstream.close()
    sys.exit(0)
                
######################################
# '-s' operation: frequency statistics
######################################

if sFlag == True:
    ## freqDict = {sourceFile: {function: freq}}
    freqDict = {}
    currentfileName = None
    for traceFile in infileList:
        infile = open(traceFile, 'r')
        for item in infile.readlines():
            if item.startswith("SF:"):
                currentfileName = item.strip()[3:]
                if currentfileName not in freqDict:
                    freqDict[currentfileName] = {}
            elif item.startswith("FNDA:"):
                item = item.strip()
                functionName = item[5:].split(',')[1]
                hitNum = int(item[5:].split(',')[0])
                # print "functionName:", functionName
                # print "hitNum:", hitNum
                if functionName not in freqDict[currentfileName]:
                    freqDict[currentfileName][functionName] = hitNum
                else:
                    freqDict[currentfileName][functionName] += hitNum


    None

    # Output format processing
    if ('-f', 'file') in optlist or '-f' not in opts:
        outlist = []
        for item in freqDict:
            freq = 0
            for sItem in freqDict[item]:
                freq += freqDict[item][sItem]
            tmpString = item + ": " + str(freq)
            outlist.append(tmpString)
        outlist.sort()

        if aggFlag == True:
            # do aggregation, then output
            paths = []
            for item in outlist:
                paths.append(item.split(':')[0])
            commPath = os.path.commonprefix(paths)


            if len(commPath) == 0:
                print >> sys.stderr, "No common path for all the source files, cannot aggregate."
                sys.exit(1)                

            # if not commPath.endswith('/'):
            #     commPath = '/'.join(commPath.split('/')[:-1]) + '/'

            # print "comm path:", commPath
            # sys.exit(1)
            
            print "commPath:", commPath
            
            aggDict = {}
            for item in outlist:
                path = item.split(':')[0]
                count = int(item.split(':')[1])
                path = path.replace(commPath, '', 1)
                path = path.split('/')[0]
                # print path
                if path not in aggDict:
                    aggDict[path] = count
                else:
                    aggDict[path] += count

            # for item in aggDict:
                # print >> outstream, item, aggDict[item]
            for item in aggDict:
                outstream.write(item + ' & ')
            outstream.write('\n')
            for item in aggDict:
                outstream.write(str(aggDict[item]) + ' & ')

        else:
            for item in outlist:
                print >> outstream, item


    elif ('-f', 'function') in optlist:
        outlist = [item for item in freqDict]
        outlist.sort()
        for item in outlist:
            print >> outstream, "FILE: " + item
            sOutlist = [sItem for sItem in freqDict[item]]
            sOutlist.sort()
            for sItem in sOutlist:
                tmpString = '\t' + sItem + ': ' + str(freqDict[item][sItem])
                print >> outstream, tmpString
                
    else:
        print >> sys.stderr, "Wrong argument given to '-f' option."
        errorInfo()
        
    sys.exit(0)

#######################################################
# '--cov-dist' operation: coverage overlap distribution
#######################################################

if dFlag == True:
    ## brFreqDict = {sourceFile: {(br1, br2, br3): freq}}
    ## lFreqDict = {sourceFile: {line: freq}}    
    brFreqDict = {}
    fFreqDict = {}    
    lFreqDict = {}
    currentfileName = None
    for traceFile in infileList:
        infile = open(traceFile, 'r')
        for item in infile.readlines():
            if item.startswith("SF:"):
                currentfileName = item.strip()[3:]
                if currentfileName not in fFreqDict:
                    fFreqDict[currentfileName] = {}
                if currentfileName not in lFreqDict:
                    lFreqDict[currentfileName] = {}
                if currentfileName not in brFreqDict:
                    brFreqDict[currentfileName] = {}
            elif item.startswith("FNDA:"):
                item = item.strip()
                functionName = item[5:].split(',')[1]
                hitNum = int(item[5:].split(',')[0])


                if functionName not in fFreqDict[currentfileName]:
                    fFreqDict[currentfileName][functionName] = 0
                if hitNum != 0:
                    fFreqDict[currentfileName][functionName] += 1
                    # print "bingo 1"
            elif item.startswith("BRDA:"):
                item = item.strip()
                brData = item[5:].split(',')
                brName = (brData[0], brData[1], brData[2])
                if brData[3] == '-' or brData[3] == '0':
                    brHit = 0
                else:
                    brHit = int(brData[3])

                if brName not in brFreqDict[currentfileName]:
                    brFreqDict[currentfileName][brName] = 0
                if brHit != 0:
                    brFreqDict[currentfileName][brName] += 1
                    # print "bingo 2"
            elif item.startswith("DA:"):
                item = item.strip()
                lineNum = item[3:].split(',')[0]
                hitNum = int(item[3:].split(',')[1])

                if lineNum not in lFreqDict[currentfileName]:
                    lFreqDict[currentfileName][lineNum] = 0
                if hitNum != 0:
                    lFreqDict[currentfileName][lineNum] += 1
                


    totalLine = 0
    totalBr = 0
    totalFun = 0
    numTracefile = len(infileList)
    hitLineCount = {}
    hitBrCount = {}
    hitFunCount = {}

    # hit times count
    for i in range(1, numTracefile + 1):
        hitLineCount[i] = 0
        hitBrCount[i] = 0
        hitFunCount[i] = 0

    for item in lFreqDict:
        for sItem in lFreqDict[item]:
            totalLine += 1
            hitTimes = lFreqDict[item][sItem]
            if hitTimes != 0:
                hitLineCount[hitTimes] += 1
    for item in brFreqDict:
        for sItem in brFreqDict[item]:
            totalBr += 1
            hitTimes = brFreqDict[item][sItem]
            if hitTimes != 0:
                hitBrCount[hitTimes] += 1
    for item in fFreqDict:
        for sItem in fFreqDict[item]:
            totalFun += 1
            hitTimes = fFreqDict[item][sItem]
            if hitTimes != 0:
                hitFunCount[hitTimes] += 1


    for i in range(1, numTracefile + 1):
        print >> outstream, "lines hit", i, "times:", float(hitLineCount[i])/float(totalLine) * 100, '%'
    print >> outstream, ""
    for i in range(1, numTracefile + 1):
        print >> outstream, "funcs hit", i, "times:", float(hitFunCount[i])/float(totalFun) * 100, '%'
    print >> outstream, ""
    for i in range(1, numTracefile + 1):        
        print >> outstream, "br hit", i, "times:", float(hitBrCount[i])/float(totalBr) * 100, '%'
    print >> outstream, ""

    # raw_input("enter any key ...")
    # print brFreqDict
    # raw_input("enter any key ...")
    # print lFreqDict
    # raw_input("enter any key ...")
    # print fFreqDict
#######################################################
# '--diff' operation: coverage difference, A.info - B.info
#######################################################

if diffFlag == True:
    if len(infileList) != 2:
        print >> stderr, "Error, exactly TWO tracefiles should be added to calculate the coverage difference."
        errorInfo()

    brFreqDictA = {}
    brFreqDictB = {}
    brFreqDict = []
    brFreqDict.append(brFreqDictA)
    brFreqDict.append(brFreqDictB)
    
    fFreqDictA = {}
    fFreqDictB = {}
    fFreqDict = []
    fFreqDict.append(fFreqDictA)
    fFreqDict.append(fFreqDictB)    

    lFreqDictA = {}
    lFreqDictB = {}
    lFreqDict = []
    lFreqDict.append(lFreqDictA)
    lFreqDict.append(lFreqDictB)

    currentfileName = None

    for i in range(0,2):
        infile = open(infileList[i])
        for item in infile.readlines():
            if item.startswith("SF:"):
                currentfileName = item.strip()[3:]
                if currentfileName not in fFreqDict[i]:
                    fFreqDict[i][currentfileName] = {}
                if currentfileName not in lFreqDict[i]:
                    lFreqDict[i][currentfileName] = {}
                if currentfileName not in brFreqDict[i]:
                    brFreqDict[i][currentfileName] = {}
            elif item.startswith("FNDA:"):
                item = item.strip()
                functionName = item[5:].split(',')[1]
                hitNum = int(item[5:].split(',')[0])


                if functionName not in fFreqDict[i][currentfileName]:
                    fFreqDict[i][currentfileName][functionName] = 0
                if hitNum != 0:
                    fFreqDict[i][currentfileName][functionName] += 1
                    # print "bingo 1"
            elif item.startswith("BRDA:"):
                item = item.strip()
                brData = item[5:].split(',')
                brName = (brData[0], brData[1], brData[2])
                if brData[3] == '-' or brData[3] == '0':
                    brHit = 0
                else:
                    brHit = int(brData[3])

                if brName not in brFreqDict[i][currentfileName]:
                    brFreqDict[i][currentfileName][brName] = 0
                if brHit != 0:
                    brFreqDict[i][currentfileName][brName] += 1
                    # print "bingo 2"
            elif item.startswith("DA:"):
                item = item.strip()
                lineNum = item[3:].split(',')[0]
                hitNum = int(item[3:].split(',')[1])

                if lineNum not in lFreqDict[i][currentfileName]:
                    lFreqDict[i][currentfileName][lineNum] = 0
                if hitNum != 0:
                    lFreqDict[i][currentfileName][lineNum] += 1
            
    totalLine = 0
    totalBr = 0
    totalFun = 0

    lineHit = 0                         # line # hit by A but not B
    brHit = 0
    funHit = 0
    # numTracefile = len(infileList)
    # hitLineCount = {}
    # hitBrCount = {}
    # hitFunCount = {}


    for item in lFreqDict[0]:
        for sItem in lFreqDict[0][item]:
            totalLine += 1
            hit_1 = lFreqDict[0][item][sItem]
            if hit_1 != 0:              # hit in A
                if item not in lFreqDict[1] or \
                   sItem not in lFreqDict[1][item] or \
                   lFreqDict[1][item][sItem] == 0:
                    lineHit += 1

    for item in brFreqDict[0]:
        for sItem in brFreqDict[0][item]:
            totalBr += 1
            hit_1 = brFreqDict[0][item][sItem]
            if hit_1 != 0:
                if item not in brFreqDict[1] or \
                   sItem not in brFreqDict[1][item] or \
                   brFreqDict[1][item][sItem] == 0:
                    brHit += 1


    for item in fFreqDict[0]:
        for sItem in fFreqDict[0][item]:
            totalFun += 1
            hit_1 = fFreqDict[0][item][sItem]
            if hit_1 != 0:
                if item not in fFreqDict[1] or \
                   sItem not in fFreqDict[1][item] or \
                   fFreqDict[1][item][sItem] == 0:
                    funHit += 1

    print >> outstream, "total line:", totalLine
    print >> outstream, "total branch:", totalBr
    print >> outstream, "total functions:", totalFun
    print >> outstream, "line difference:", (1.0 * lineHit / totalLine)
    print >> outstream, "branch difference:", (1.0 * brHit / totalBr)
    print >> outstream, "function difference:", (1.0 * funHit / totalFun)
