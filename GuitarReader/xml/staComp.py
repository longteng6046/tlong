##################################################
#
# File: staComp.py
# Description:
#   compare the state files of the same guitar test cases, record the
#   differences. 
#
##################################################

import sys
import os

# from lxml import etree
# from lxml import objectify

# from staCompHelper import *

from myxml import *



if len(sys.argv) != 3:
    print >> sys.stderr, "Error."
    print >> sys.stderr, "\tFormat: python ./staComp.py DIR1/TO/TESTS DIR2/TO/TESTS"
    sys.exit(1)


dir1 = sys.argv[1]
dir2 = sys.argv[2]

testList = os.listdir(dir1)
testListCheck = os.listdir(dir2)

if testListCheck != testList:
    print >> sys.stderr, "Error."
    print >> sys.stderr, "The two directories are containing different tests"
    sys.exit(1)



counter = 0

for item in testList:

    counter += 1
    if counter - counter / 10 * 10 == 0:
        print "counter:", counter

    file1 = open(dir1 + '/' + item)
    file2 = open(dir2 + '/' + item)

    
    xtree1 = Xtree()
    xtree2 = Xtree()

    xtree1.parseFile(file1)
    xtree2.parseFile(file2)
    
    xtree1.formalize()
    xtree2.formalize()


    diffTree(xtree1.root, xtree2.root)



    file1.close()
    file2.close()
