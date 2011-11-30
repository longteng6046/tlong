#!/usr/bin/python

import sys
import os

if len(sys.argv) != 3:
    print >> sys.stderr, "./" + sys.argv[0] + " source_dir dest_dir"
    sys.exit(1)

srcdir = sys.argv[1]
desdir = sys.argv[2]

fileList = os.listdir(srcdir)
# print fileList

fd_des = open(desdir, 'w')

for infile in fileList:

    # print infile
    values = open(srcdir + '/' + infile).xreadlines()

    # print >> fd_des, infile[:-4]

    fd_des.write(infile[:-4])
    fd_des.write(" : ")
    
    valSet = set([])
    for item in values:
        item = item.strip()
        # print item
        if '.' in item:
            valSet.add(float(item))
        else:
            valSet.add(int(item))


    # print >> fd_des, '(', min(valSet), ',', max(valSet), ')'

    scale = '(' + str(min(valSet)) + ',' + str(max(valSet)) + ')' + '\n'
    
    fd_des.write(scale)
    
    print >> fd_des, len(valSet)
    # for item in valSet:
        # print >> fd_des, item

    print >> fd_des, ""
