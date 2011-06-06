##################################################
#
# File: covReader
# Description:
#   A better-performance difference analysis tool.
#    It reads converage.xml files in each test report,
#    Then put them all in a dictionary, and save the
#    dictionary to a file named "covDict.dic".
#
##################################################

import sys
import os
import pickle
from mine import *
from covReaderHelper import *

########################################
#
# Coverage data read
#
########################################

## control flags enable/disable functions.
tcCheck = True # Check whether test cases under each directory are of
                # the same name.
                

print "****** Caution: The parent directories holding test report sets should not be the same. ******"



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
    else:
        print "Error, the following directory does not exits:\n\t", sys.argv[i]
        sys.exit(1)
        
# printl(dirList)



# file dictionary of files under all directories in dirList

fileDict = {} # fileDict = {dirList, {coverage.xml, {pkgname, {classFile, {covType, data}}}}}
# print "dirList: ", dirList

for item in dirList:
    testList = os.listdir(item)
    # printl(testList)

    subDict = {}
    for sItem in testList:
        covFile = os.path.abspath(item + '/' + sItem + '/coverage.xml')
        # print covFile
        subDict[covFile] = None

    fileDict[item] = subDict

##############################
#
# Check whether the test cases under each directory is the same
#
##############################

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
        

##############################
#
# Clear up the dictionary name
#
##############################

# print "---------- Test area ----------"


dirs = fileDict.keys()
tests = []
for item in fileDict.keys():
    tests = fileDict[item].keys()
    break

testSample = tests[0]
baseDir = testSample.split('/')[:-3]
baseDir = '/'.join(baseDir) + '/' # path to coverage.xml: baseDir + dirname + testname + 'coverage.xml'


newFileDict = {}
for item in tests:

    item = item.split('/')[-2]
    
    tmpDict = {}
    for sItem in dirs:
        sItem = sItem.split('/')[-1]
        # print sItem
        tmpDict[sItem] = None
    newFileDict[item] = tmpDict

# for item in newFileDict:
    # print item, newFileDict[item]
# exit()    

##############################
#
# Read coverage.xml files, new
#
##############################
counter = 0

for item in newFileDict:
    counter += 1
    if counter - counter / 10 * 10 == 0:
        print "... Processing test", counter
    for sItem in newFileDict[item].keys(): # reaching each individual
                                        # coverage.xml file
        # print sItem
        
        path = baseDir + '/' + sItem + '/' + item + '/coverage.xml'

        # print "Path: ", path
        # exit()
        
        covFileLines = open(path, 'r')

        # print "item:", item, "sItem", sItem


        newFileDict[item][sItem] = covFileProcess(covFileLines)
        covFileLines.close()


print "Coverage data collection finished."





##############################
#
# Save the coverage dictionary to a file
#
##############################

print "Begin to save info to the dictionary..."

covDictFile = open("covDict.dic", 'w')
pickle.dump(newFileDict, covDictFile)
covDictFile.close()

print "Finished saving."
