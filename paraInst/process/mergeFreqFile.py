#!/usr/bin/python

import sys
import os

if len(sys.argv) != 4:
    print >> sys.stderr, "Error. Usage: python mergeFreqFile.py srcFile1 srcFile2 destFile"
    sys.exit(-1)


src1 = open(sys.argv[1])    
src2 = open(sys.argv[2])

freqDict = {}                           # {func_para, {value, freq}}

for line in src1.readlines():
    name, value, freq = line.split()
    freq = int(freq)

    if name not in freqDict:
        freqDict[name] = {}

    if value not in freqDict[name]:
        freqDict[name][value] = freq
    else:
        freqDict[name][value] += freq


for line in src2.readlines():
    name, value, freq = line.split()
    freq = int(freq)

    if name not in freqDict:
        freqDict[name] = {}

    if value not in freqDict[name]:
        freqDict[name][value] = freq
    else:
        print name
        freqDict[name][value] += freq


des = open(sys.argv[3], 'w')

for item in freqDict:
    for sItem in freqDict[item]:
        print >> des, item, sItem, freqDict[item][sItem]
