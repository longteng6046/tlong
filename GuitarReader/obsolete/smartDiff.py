#!/usr/bin/python
#****************************************
#
# Filename: smartDiff.py
# Func: find the differences between coverage files.
#       Good to all cov.xml files from Guitar
#
#****************************************

import sys
import os
import re
import pickle

if len(sys.argv) == 1:
    print "\tformat error."

    print "Format: python ./diff.py dir1 dir2 dir3 ... dirn"
    print "\tdir1~dirn are directories that contains individual coverage reports of all test cases."
    sys.exit(1)

dirList = []
nameList = []
for i in range(1, len(sys.argv)):
    if os.path.exists(sys.argv[i]) == True:
        nameList.append(sys.argv[i])
        dirList.append(os.path.abspath(sys.argv[i]))

numFile = len(os.listdir(dirList[0]))
for i in range(1, len(dirList)):
    if len(os.listdir(dirList[i])) != numFile:
        print "All directories should have the same number of test cases."
        sys.exit()

subDirList = os.listdir(dirList[0]) # use the first directory as the

# For each test case from different environments, do the following steps:
# Step 1: Check whether each coverage.xml has the same structure
#         by comparing the number of lines in them;
# Step 2: simultaneously scan all files, comparing lines one by one.
# Step 3: Put the name of disagreed Classes and methods into a universal structure.

errorList = {} # (ClassName, methodName): [(TestCase, version_pair[(1, 2, lineNumber), ]), ]

for i in range(0, len(subDirList)):
    caseName = subDirList[i]
    fileList = [] # the list that contains opened coverage xml files
    iterList = [] # a list of iterators from the files
    for dir in dirList:
        path = dir + "/" + caseName + "/coverage.xml"
        tmpFile = open(path)
        fileList.append(tmpFile)
        iterList.append(tmpFile.readlines())

    fileFormatFlat = True # saying that all xml files have the same # of lines, by default
    for j in range(0, len(iterList) - 1):
        if len(iterList[j]) != len(iterList[j + 1]):
            fileFormatFlat = False
            break

    if fileFormatFlat == False:
        print "Test case", caseName, "has different xml formats in different directories."
        continue

    # The case when the all have the same xml structure
    #  define 3 marks
    pkg_name = "N/A"
    class_name = "N/A"
    method_name = "N/A"

    diffFlag = None # flag indicating that all cases have the same coverage

    for j in range(0, len(iterList[0])): # for each line
        if diffFlag == False: # No overall coverage difference between all the testcases
            break
        lineList = [] # a list of lines from each xml file
        for item in iterList:
            lineList.append(item[j])
            
        sample = lineList[0].strip() # get a sample of lineList
        if sample.startswith("<coverage "): # it is the line saying the overall coverage
            covList = []
            for item in lineList:
                line_covered = int(re.findall(r'lines-covered="([\d]+)"', item)[0]) # line coverage
                covList.append(line_covered)
                        
            for k in range(0, len(covList) - 1):
                if covList[k] != covList[k + 1]:
                    diffFlag = True
                    break
            continue

        elif sample.startswith("<package name="):
            pkg_name = re.findall(r'package name="([\S]+)"', sample)[0] # set package name
            continue

        elif sample.startswith("<class name="):
            class_name = re.findall(r'class name="([\S]+)"', sample)[0] # set package name
            continue
        elif sample.startswith("<method name="):
            method_name = re.findall(r'method name="([\S]+)"', sample)[0] # set package name
            # print "pkg_name:", pkg_name, "class_name:", class_name, "method_name:", method_name
        elif sample.startswith("<line number="):
            hitsCov = []
            for item in lineList:
                hit = int(re.findall(r'hits="([\d]+)"', item)[0]) # line coverage
                line_num = int(re.findall(r'line number="([\d]+)"', item)[0]) # line coverage
                if hit != 0:
                    hitsCov.append(True)
                else:
                    hitsCov.append(False)

            ver_pair_list = []
            key = (class_name, method_name)

            for k in range(0, len(hitsCov)):
                for m in range(k + 1, len(hitsCov)):
                    if hitsCov[k] != hitsCov[k + 1]: # find an unmatch line
                        pair = (nameList[k], nameList[m], line_num)
                        ver_pair_list.append(pair)
            if len(ver_pair_list) != 0:
                element = (caseName, ver_pair_list)
                if key in errorList and (element not in errorList[key]):
                    errorList[key].append(element)
                else:
                    errorList[key] = [element]
            continue
                        

    for item in fileList:
        item.close()
# The errorList contains pretty much everything we need.
# print "errorList:"
# for item in errorList:
    # print '(', item, ':\n\t', errorList[item], ')'



# Output the result into a file
outfile = open("difference.dat", 'wb')
pickle.dump(errorList, outfile)
outfile.close()

