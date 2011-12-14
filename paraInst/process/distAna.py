#!/usr/bin/python

import sys
import os

if len(sys.argv) < 2:
    print >> sys.stderr, "Usage: python", sys.argv[0], "self_freq.txt other_freq.txt ..."
    sys.exit(1)



paraDict = {}                           # {parameter : {value : {filename: freq}}}

paraCovDict = {}                        # {parameter: {filename: 1}}

for i in range(1, len(sys.argv)):
    filename = sys.argv[i]
    lines = open(filename).xreadlines()
    for line in lines:
        line = line.strip()
        # print line
        paraname, value, freq = line.split()

        if '.' not in value:
            value = int(value)
        else:
            value = float(value)

        freq = int(freq)
    
        # print paraname, value, freq
        if paraname not in paraDict:
            paraDict[paraname] = {}
        if value not in paraDict[paraname]:
            paraDict[paraname][value] = {}
        if filename not in paraDict[paraname][value]:
            paraDict[paraname][value][filename] = freq

        if paraname not in paraCovDict:
            paraCovDict[paraname] = {}
        if filename not in paraCovDict[paraname]:
            paraCovDict[paraname][filename] = 1

for item in paraDict:
    if len(paraCovDict[item]) != 3:
        continue

    print "--------------------------------------------------------------------------------"
    print item
    valueDict = paraDict[item]          # {value: {filename: freq}}

    # find out all hits
    values = []
    for sitem in valueDict:
        values.append(sitem)
    values.sort()
    
    # for sitem in values:
    #     print sitem

    print values[0], values[-1]

    num_piece = 10
    
    scale = values[-1] - values[0] + num_piece
    
    for i in range(0, num_piece):
        min = values[0] + i * scale / num_piece
        max = values[0] + (i+1) * scale / num_piece


        
        count = 0
        freqDict = {}
        for v in values:
            if v >= min and v < max:
                count += 1
                for filename in valueDict[v]:
                    if filename not in freqDict:
                        freqDict[filename] = valueDict[v][filename]
                    else:
                        freqDict[filename] += valueDict[v][filename]                    # print filename, valueDict[v][filename]
                    freq += valueDict[v][filename]
        if count == 0:
            continue
        print '[', min, ',', max, ')'
        print "count:", count
        if len(freqDict) != 0:
            print "freq:"
        for filename in freqDict:
            print filename, freqDict[filename]

        print ''
            
    

    
    # find out the scale of this value

    
