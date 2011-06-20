##################################################
#
# File: formalize.py
# Description:
#   Formalize the xml files to be in the sorted order
#   
#
##################################################

import sys
import os
import codecs

# from staCompHelper import *
from myxml import *



if len(sys.argv) != 3:
    print >> sys.stderr, "Error."
    print >> sys.stderr, "\tFormat: python ./formalize.py DIR/TO/xml/FILES DIR/TO/SAVE"
    sys.exit(1)


dir1 = sys.argv[1]
dir2 = sys.argv[2]

testList = os.listdir(dir1)

counter = 0

for item in testList:
    counter += 1
    xmlfile = codecs.open(dir1 + '/' + item, encoding='utf-8', mode='r')


    if len(xmlfile.readlines()) < 10:
        continue

    destfile = codecs.open(dir2 + '/' + item, encoding='utf-8', mode='w')
    xmlfile.seek(0)
    
    xtree = Xtree()
    print "case:", item
    xtree.parseFile(xmlfile)
    xtree.formalize()
    writeXML(xtree.root, destfile)

    xmlfile.close()
    destfile.close()

    if counter - counter / 10 * 10 == 0:
        print counter
