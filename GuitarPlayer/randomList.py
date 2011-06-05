#!/usr/bin/python

import sys
import os
import random

if len(sys.argv) != 3:
    print "Format: randomize.py Dir_Name #cases\n"
    exit()
dirName = sys.argv[1]
# print "ls " + dirName
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





cases = cache.split(',')

random.shuffle(cases)

testlist = ''

num = int(sys.argv[2])
counter = 0

if num > len(cases):
    print "No enough test cases in the directory."
    sys.exit(1)
    

for item in cases:
    testlist += item
    counter +=1
    if counter == num:
        break
    testlist += ','

print testlist
