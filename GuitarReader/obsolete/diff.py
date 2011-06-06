#!/usr/bin/python
#****************************************
#
# Filename: diff.py
# Func: find the differences between two coverage files.
#
#****************************************

import sys
import os
import re

if len(sys.argv) == 1:
    print "\tformat error."

    print "Format: python ./diff.py dir1 dir2 dir3 ... dirn"
    print "\tdir1~dirn are directories that contains individual coverage reports of all test cases."


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
        sys.exit(0)

subDirList = os.listdir(dirList[0]) # use the first directory as the 

for item in subDirList: # FOR each tet case:
    caseName = item
    covList = [] # the list that contains opened coverage xml files
    for dir in dirList:
        path = dir + "/" + item + "/coverage.xml"
        tmpFile = open(path)
        covList.append(tmpFile)
        
    # Assume all the coverage.xml files are exactly the same except
    # coverage data

    # Compare overall coverage first
    # Using line_coverage as the comparing factor ******************************
    overall_cov = [] # a list of overall coverages for each coverage file
    core_cov = []
    gui_cov = []
    filter_cov = []
    for cov in covList:
        lines = cov.readlines()
        for i in range(0, len(lines)):
            if "<coverage " in lines[i]:
                line_covered = int(re.findall(r'lines-covered="([\d]+)"', lines[i])[0]) # line coverage
                overall_cov.append(line_covered)
            elif '<package name="org.cesilko.rachota.core"' in lines[i]:
                line_covered = float(re.findall(r'line-rate="([\d|.]+)"', lines[i])[0]) # line coverage
                core_cov.append(line_covered)
                # overall_cov.append(line_covered)
            elif '<package name="org.cesilko.rachota.core.filters"' in lines[i]:
                line_covered = float(re.findall(r'line-rate="([\d|.]+)"', lines[i])[0]) # line coverage
                filter_cov.append(line_covered)
            elif '<package name="org.cesilko.rachota.gui"' in lines[i]:
                line_covered = float(re.findall(r'line-rate="([\d|.]+)"', lines[i])[0]) # line coverage
                gui_cov.append(line_covered)

            

    # overall_cov = [1,1,1]
    # print overall_cov

    flag = True # assume all cov.xml has the same line coverage at first
    for i in range(0, len(overall_cov)):
        for j in range((i + 1), len(overall_cov)):
            if overall_cov[i] == overall_cov[j]:
                continue
            else:
                flag = False
                print "Line cov of", caseName, "is different in:",  nameList[i], "and", nameList[j]


    if flag == True: # means the coverage are all the same under different platforms
        break
    else: # means overall coverage are DIFFERENT
        # print "overall_coverage: ", overall_cov
        # print "core: ", core_cov
        # print "gui: ", gui_cov
        # print "filter: ", filter_cov

        flag = True # assume all cov.xml has the same line coverage at first
        for i in range(0, len(core_cov)):
            for j in range((i + 1), len(core_cov)):
                if core_cov[i] - core_cov[j] < 0.00001:
                    continue
                else:
                    flag = False
                    print "Core: cov of", caseName, "is different in:",  nameList[i], "and", nameList[j]

        for i in range(0, len(gui_cov)):
            for j in range((i + 1), len(gui_cov)):
                if gui_cov[i] - gui_cov[j] < 0.00001:
                    continue
                else:
                    flag = False
                    print "Gui: cov of", caseName, "is different in:",  nameList[i], "and", nameList[j]
        for i in range(0, len(filter_cov)):
            for j in range((i + 1), len(filter_cov)):
                if filter_cov[i] - filter_cov[j] < 0.00001:
                    continue
                else:
                    flag = False
                    print "Filter: cov of", caseName, "is different in:",  nameList[i], "and", nameList[j]
