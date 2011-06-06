##################################################
#
# File: newDiff.py
# Description:
#   A better-performance difference analysis tool.
#
##################################################

import sys
import os
import pickle
from mine import *
from newDiffHelper import *

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

# for item in newFileDict:
#     print "Test:", item
#     print "Content:"
#     for sItem in newFileDict[item]:
#         print sItem, newFileDict[item][sItem]



# exit()



# ##############################
# #
# # Read coverage.xml files
# #
# ##############################
# for item in fileDict:
#     for sItem in fileDict[item].keys(): # reaching each individual
#                                         # coverage.xml file
#         # print sItem

#         covFileLines = open(sItem, 'r')

#         sItem = sItem.split('/')[-2]
#         # print sItem
#         # exit()

#         fileDict[item][sItem] = covFileProcess(covFileLines)
#         covFileLines.close()

#         # for ssItem in fileDict[item][sItem].keys():
#         #     print "pkgName: ", ssItem
#         #     print "classes: "
#         #     classDict = fileDict[item][sItem][ssItem]
#         #     for i in classDict.keys():
#         #         print i, "lineCov:", classDict[i]["lineCov"], "branchCov:", classDict[i]["branchCov"]
        
#         # exit()

# print "Coverage data collection finished."




##############################
#
# Save the coverage dictionary to a file
#
##############################

covDictFile = open("covDict.dic", 'w')
pickle.dump(newFileDict, covDictFile)
covDictFile.close()

exit()


# for item in fileDict[0][0]:
    # numClass += len(fileDict[0][0][item])

l = []

for item in fileDict.keys():

    for sItem in fileDict[item].keys():
        numClass = 0 # Number of classes
        for ssItem in fileDict[item][sItem].keys():
            numClass += len(fileDict[item][sItem][ssItem])
        l.append(numClass)

for i in range(0, len(l) -1):
    if l[i] != l[i+1]:
        print "False"
        exit()
print "True"        
        
