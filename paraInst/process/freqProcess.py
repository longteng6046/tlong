#!/usr/bin/python

import sys
import os

if len(sys.argv) != 3:
    print >> sys.stderr, "./" + sys.argv[0] + " source_dir dest_file"
    sys.exit(1)

srcdir = sys.argv[1]
destfile = sys.argv[2]

fileList = os.listdir(srcdir)

fd_des = open(destfile, 'w')

for infile in fileList:
    valueDict = {}
    values = open(srcdir + '/' + infile).xreadlines()
    for value in values:
        value = value.strip()
        if value not in valueDict:
            valueDict[value] = 1
        else:
            valueDict[value] += 1
    for item in valueDict:
        print >> fd_des, infile, item, valueDict[item]
        

