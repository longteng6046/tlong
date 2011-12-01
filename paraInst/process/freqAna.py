#!/usr/bin/python

import sys
import os

if len(sys.argv) <= 2:
    print >> sys.stderr, "Error!\nUsage: python freqAna.py dir1, dir2, ..., dirn"
    sys.exit(-1)

num_dir = len(sys.argv) - 1

fileDict = {}                   # {fun_name_parameter: {pkg_name: {value, freq}}}


for i in range(1, num_dir + 1):
    pkg_name = sys.argv[i]
    fd_infile = open(pkg_name)

    for line in fd_infile:
        name, value, freq = line.split()
        
        if name not in fileDict:
            fileDict[name] = {}
        if pkg_name not in fileDict[name]:
            fileDict[name][pkg_name] = {}
        if value in fileDict[name][pkg_name]:
            print >> sys.stderr, "What freq of this paremeter already there?"
            sys.exit(-1)
        else:
            fileDict[name][pkg_name][value] = freq
        
print "There are", len(fileDict.keys()), "parameters being covered by all."



counter = 0

for item in fileDict:
    if len(fileDict[item].keys()) == 1:
        continue
    else:
        pkg_names = fileDict[item].keys()
        selfName = None
        petscName = None
        otherNames = []
        for name in pkg_names:
            if "self" in name:
                selfName = name
            elif "petsc" in name:
                petscName = name
            else:
                otherNames.append(name)
        
        covered_values = fileDict[item][selfName].keys()
        if petscName != None:
            covered_values2 = fileDict[item][petscName].keys()
            covSet = set()
            for val in covered_values:
                covSet.add(val)
            for val in covered_values2:
                covSet.add(val)
        flag = 0
        pkgCntDict = {}

        for pkg in otherNames:
            upper_values = fileDict[item][pkg].keys()
            count = 0
            for v in upper_values:
                if v not in covSet:
                    count += 1
            if count != 0:
                flag = 1
            if count != 0:
                pkgCntDict[pkg] = count
        if flag == 1:
            counter += 1
            print counter
            print item
            print "size of covered values:", len(covered_values)
            for pkg in pkgCntDict:
                print pkg, pkgCntDict[pkg]
            print '--------------------------------------------------------------------------------'
    # selfName = None


    # print item
    # for key in fileDict[item].keys():
    #     print key, len(fileDict[item][key])
    # counter += 1

print "#:", counter

