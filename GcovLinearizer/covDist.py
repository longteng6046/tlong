
#
# File: covDist.py
# Description:
#   1. This script analyzes the coverage distribution of 
#      different upper-level packages.
#   2. coverage is 
#   
##############################

import sys
import os

from covDisthelper import *

##############################
#
# Coverage data read
#
##############################


# Step 1: get the .info file list.

if len(sys.argv) != 2:
    print >> sys.stderr, "Error: Format: python covLinear.py DIR/TO/.INFO/FILES"
    # print "This goes to the stdout."
    sys.exit(1)

fileDir = os.path.abspath(sys.argv[1])

# print "file path: ", fileDir

infoList = []

for item in os.listdir(fileDir):
    if ".info" in item and not "~" in item and not "#" in item:
        item = fileDir + '/' + item
        infoList.append(item)

infoList.sort()

contentList = {}
for item in infoList:
    # print item
    contentList[item] = open(item, 'r')

# print contentList

# Step 2: scan .info files, store coverage data
# Coverage data:
#  lineCovData = { fileName, {sourceFile, {line#, hit_times}} }
#  funCovData = { fileName, {sourceFile, {func_name, hit_times}} }
#  brCovData = { fileName, {sourceFile, {(line#, block#, br#), hit_times}} }
#  
# Summary data:
# key: 'found', 'hit'; val: int
#  lineSum = {fileName, {sourceFile, {key, val}}}
#  funSum = {fileName, {sourceFile, {key, val}}}
#  brSum = {fileName, {sourceFile, {key, val}}}


lineCovData = {}
funCovData = {}
brCovData = {}

lineSum = {}
funSum = {}
brSum = {}

for item in contentList:

    if item not in lineCovData:
        lineCovData[item] = {}
        funCovData[item] = {}
        brCovData[item] = {}

        lineSum[item] = {}
        funSum[item] = {}
        brSum[item] = {}
    content = contentList[item].readlines()


    # status flags for each file
    sourceFile = '' # the abspath to the source file
    isCFile = False # indicating whether it is a .c file


    # for each file
    for line in content:

        line = line.strip()

        if line.startswith('SF:'):
            sourceFile = line[3:]
            if sourceFile.endswith('.c'):
                isCFile = True
                if sourceFile not in lineCovData[item]:
                    lineCovData[item][sourceFile] = {}
                    funCovData[item][sourceFile] = {}
                    brCovData[item][sourceFile] = {}

                    lineSum[item][sourceFile] = {}
                    funSum[item][sourceFile] = {}
                    brSum[item][sourceFile] = {}
                else:
                    print >> sys.stderr, "Error: duplicated source file:"
                    print >> sys.stderr, "Filename: ", item
                    print >> sys.stderr, "Source file name: ", sourceFile
                    # sys.exit(1)
                    continue
            elif sourceFile.endswith('.h'):
                isCFile = False
                continue
            elif sourceFile.endswith('.l'): # lex
                isCFile = False
                continue
            else:
                print >> sys.stderr, "Error: wired filename..."                
                print >> sys.stderr,  sourceFile
                isCFile = False
                continue
                # sys.exit(1)

        # if it is currently a '.h' file, then skip the current line
        elif isCFile == False:
            continue

        elif line.startswith('FN:'):
            funName = line.split(',')[1]
            # print funName
            # print line
            funCovData[item][sourceFile][funName] = None
            continue
        
        elif line.startswith('FNDA:'):
            funName = line.split(',')[1]
            hitTimes = line.split(',')[0].split(':')[1]
            # print "item:", item, "sourceFile:", sourceFile
            # print "funName:", funName

            # gcov bug, sometimes the function name will not be
            # detected, but this hitting record will be recorded.
            if funName not in funCovData[item][sourceFile]: 
                funCovData[item][sourceFile][funName] = None
            if funCovData[item][sourceFile][funName] == None:
                funCovData[item][sourceFile][funName] = int(hitTimes)
            else:
                print >> sys.stderr, "Error: muliple function hit record."
                print >> sys.stderr, "file: ", item
                print >> sys.stderr, "source file: ", sourceFile
                print >> sys.stderr, "function name: ", funName
                sys.exit(1)
            continue

        elif line.startswith('FNF:'):
            funSum[item][sourceFile]['found'] = int(line[4:])
            continue

        elif line.startswith('FNH:'):
            # print int(line[4:])
            funSum[item][sourceFile]['hit'] = int(line[4:])

        elif line.startswith('BRDA:'):
            data = line[5:].split(',')
            key = (data[0], data[1], data[2])
            if data[3] == '-':
                val = 0
            else:
                val = int(data[3])
            brCovData[item][sourceFile][key] = val
            continue

        elif line.startswith('BRF:'):
            brSum[item][sourceFile]['found'] = int(line[4:])
            continue

        elif line.startswith('BRH:'):
            brSum[item][sourceFile]['hit'] = int(line[4:])
            # print int(line[4:])
            continue
            
        elif line.startswith('DA:'):
            data = line[3:]
            line_num = data.split(',')[0]
            hit_num = int(data.split(',')[1])
            lineCovData[item][sourceFile][line_num] = hit_num
            continue

        elif line.startswith('LF:'):
            lineSum[item][sourceFile]['found'] = int(line[3:])
            continue

        elif line.startswith('LH:'):
            lineSum[item][sourceFile]['hit'] = int(line[3:])
            # print item, sourceFile
            # print int(line[3:])
            # print lineSum[item][sourceFile]
            continue

        else:
            continue



##############################
#
# Coverage Statistics
#
##############################


# lineStat_single = {(sourcefile, line#), isHit}
# funStat_single = {(sourcefile, func_name, isHit)}
# brStat_single = {(sourcefile, line#, block#, br#), isHit}

# lineStat = {(sourcefile, line#), hitTimes}
# funStat = {(sourcefile, func_name, hitTimes)}
# brStat = {(sourcefile, line#, block#, br#), hitTimes}

# CAUTION: we DO NOT count apr's own unit test in coverage statistics


lineStat_single = {}
funStat_single = {}
brStat_single = {}

lineStat = {}
funStat = {}
brStat = {}


# for item in lineCovData.keys():
    # print item


# example_info_file = "/home/tlong/Dropbox/func_test/openmpi_result/infofiles/freepooma.info"
# example_info_file = fileDir + "/freepooma.info"
example_info_file = infoList[0]

sourceList = lineCovData[example_info_file]


# print infoList

for item in sourceList:
    for sItem in sourceList[item]:
        key = (item, sItem)
        # print key
        val = 0
        counter = 0
        for infoFile in infoList:
            if 'self' not in infoFile:
                # print "infoFile", infoFile
                # print "infoFile:", infoFile
                # print "item:", item

                # the file is not covered at all
                if (item not in lineCovData[infoFile]) or \
                       sItem not in lineCovData[infoFile][item]:
                    continue
                val += lineCovData[infoFile][item][sItem]
                if lineCovData[infoFile][item][sItem] != 0:
                    counter += 1

        # print (key, val)
        lineStat[key] = val
        lineStat_single[key] = counter

sourceList = funCovData[example_info_file]

for item in sourceList:
    for sItem in sourceList[item]:
        key = (item, sItem)
        val = 0
        counter = 0

        for infoFile in infoList:
            if 'self' not in infoFile:
                if item not in funCovData[infoFile] or \
                       sItem not in funCovData[infoFile][item]:
                    continue
                
                val += funCovData[infoFile][item][sItem]
                if funCovData[infoFile][item][sItem] != 0:
                    counter += 1
        
        funStat[key] = val
        funStat_single[key] = counter
        # if val == 0:
        #     funStat_single[key] = 0
        # else:
        #     funStat_single[key] = 1


sourceList = brCovData[example_info_file]

for item in sourceList:
    for sItem in sourceList[item]:
        key = (item, sItem)
        val = 0
        counter = 0

        for infoFile in infoList:
            if 'self' not in infoFile:
                # print "infoFile", infoFile
                if item not in brCovData[infoFile] or \
                       sItem not in brCovData[infoFile][item]:
                    continue
                val += brCovData[infoFile][item][sItem]
                if brCovData[infoFile][item][sItem] != 0:
                    counter += 1
                
        brStat[key] = val
        brStat_single[key] = counter






# for item in lineCovData.keys():
    # singleFileDict = lineCovData[item]
    # for sItem in singleFileDict:
        # print sItem

    # break




fileNameList = lineCovData.keys()
l2 = brCovData.keys()
if fileNameList != l2:
    print "Shit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    exit()

fileNameList.sort()

print "\n---------- The list of coverage files: ----------"
print  "*************************************************"
for item in fileNameList:
    print item
print  "*************************************************\n"





# print r'''
# ########################################
# #
# # 0. Distribution for single tests -- file(all five .info)
# #
# ########################################
# '''





# print r'''
# ########################################
# #
# # 1. Distribution for single tests -- directory(all five .info)
# #
# ########################################
# '''

# for item in fileNameList:
#     print "info file:", item
    
#     covRateListL = fileCovL(lineCovData[item])
#     covRateListB = fileCovB(brCovData[item])

#     print "line:"
#     for sItem in zoom(covRateListL, 0):
#         print sItem
#     print "branch:"
#     for sItem in zoom(covRateListB, 0):
#         print sItem


# print r'''
# ########################################
# #
# # 2. Distribution for extra cov of single tests -- directory(all five .info)
# #
# ########################################
# '''

# selfIdx = len(fileNameList) - 1
# print "self:", selfIdx
# for i in range(0, len(fileNameList) - 1):
#     print "info:", fileNameList[i]
#     extraCovL = covDictExtraL(lineCovData[fileNameList[i]], lineCovData[fileNameList[selfIdx]])
#     extraCovB = covDictExtraB(brCovData[fileNameList[i]], brCovData[fileNameList[selfIdx]])    

#     covRateListL = fileCovL(extraCovL)
#     covRateListB = fileCovB(extraCovB)
#     print "line:"
#     for item in zoom(covRateListL, 2):
#         print item

#     print "Branch:"
#     for item in zoom(covRateListB, 2):
#         print item




print r'''
########################################
#
# 3. Distribution for extra cov of overall tests -- directory(all five .info)
#
########################################
'''



selfIdx = len(fileNameList) - 1
print "self:", selfIdx

d0L = lineCovData[fileNameList[0]]
d1L = lineCovData[fileNameList[1]]
d2L = lineCovData[fileNameList[2]]
d3L = lineCovData[fileNameList[3]]
d4L = lineCovData[fileNameList[4]]

d0B = brCovData[fileNameList[0]]
d1B = brCovData[fileNameList[1]]
d2B = brCovData[fileNameList[2]]
d3B = brCovData[fileNameList[3]]
d4B = brCovData[fileNameList[4]]





# coverage overlap of all 4 components
dmL = covDictAndL(d0L, d1L)
dmL = covDictAndL(d2L, dmL)
dmL = covDictAndL(d3L, dmL)

dmB = covDictAndB(d0B, d1B)
dmB = covDictAndB(d2B, dmB)
dmB = covDictAndB(d3B, dmB)

extraL = covDictExtraL(dmL, d4L)
extraB = covDictExtraB(dmB, d4B)



print "AND(overlap):"

print "line:"
for item in zoom(fileCovL(extraL), 0):
    print item
    
print "branch:"
for item in zoom(fileCovB(extraB), 0):
    print item


# coverage cumulation of all 4 components
dmL = covDictOrL(d0L, d1L)
dmL = covDictOrL(d2L, dmL)
dmL = covDictOrL(d3L, dmL)

dmB = covDictOrB(d0B, d1B)
dmB = covDictOrB(d2B, dmB)
dmB = covDictOrB(d3B, dmB)

extraL = covDictExtraL(dmL, d4L)
extraB = covDictExtraB(dmB, d4B)

print "Or(cumulation):"

print "line:"
for item in zoom(fileCovL(dmL), 0):
    print item
    
print "branch:"
for item in zoom(fileCovB(dmB), 0):
    print item



















# for item in fileNameList:
#     print "info file:", item
    
#     print "line coverage:"

#     covRateListL = fileCovL(lineCovData[item])
#     for pair in covRateListL:
#         print pair

#     print "--------------------------------------------------------------------------------"
        
#     print "Branch coverage:"
#     covRateListB = fileCovB(brCovData[item])
#     for pair in covRateListB:
#         print pair
        
    



