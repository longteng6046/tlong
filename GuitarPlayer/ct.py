#!/usr/bin/python

import sys
import os
if len(sys.argv) != 2:
    print "Format: ct.py Dir_Name\n"
    exit()
dirName = sys.argv[1]
print "ls " + dirName
os.system("ls " + dirName + " > files.txt")
infile = open("files.txt")
cache = ''
counter = 0
for item in infile.readlines():
    if counter == 0:
        cache = cache + item.strip()
        counter = 1
    else:
        cache = cache +','+item.strip()
print cache
