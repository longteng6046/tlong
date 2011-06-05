##################################################
#
# File: newDiff.py
# Description:
#   A better-performance difference analysis tool.
#
##################################################

import sys
import os
from mine import *

########################################
#
# Coverage data read
#
########################################

## control flags enable/disable functions.
tcCheck = False # Check whether test cases under each directory are of
                # the same name.
                





if len(sys.argv) == 1:
    print "Error."
    print "\tFormat: python ./newdiff.py dir1 dir2 dir3 ... dirn"
    print "\tdir1~dirn are directories that contains individual coverage \n\treports(coverage.xml) of all test cases."
    sys.exit(1)

# list of different directories
dirList = []

for i in range(1, len(sys.argv)):
    if os.path.exists(sys.argv[i]) == True:
        dirList.append(os.path.abspath(sys.argv[i]))

# printl(dirList)



# file dictionary of files under all directories in dirList

fileDict = {} # fileDict = {dirList, {coverage.xml, {pkgname, {classFile, {covType, data}}}}}
for item in dirList:
    testList = os.listdir(item)
    # printl(testList)

    subDict = {}
    for sItem in testList:
        covFile = os.path.abspath(item + '/' + sItem + '/coverage.xml')
        # print covFile
        subDict[covFile] = None

    fileDict[item] = subDict


# Check whether the test cases under each directory is the same

if tcCheck == True:
    compList = []

    for item in fileDict.keys():
        files = fileDict[item].keys()
        files.sort()
        subList = []
        for sItem in files:
            casename = sItem.split('/')[-2:-1]
            subList.append(casename)
        compList.append(subList)

    for i in range(0, len(compList)):
        for j in range(i + 1, len(compList)):
            # print "i:", i, "j", j
            # print compList[i]
            # print compList[j]

            if compList[i] != compList[j]:
                print "bala"
                exit()
        
    print "Finished testcases name checking."    
        
