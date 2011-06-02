#!/usr/bin/python
# **********************************************************************
# Filename: showResult.py
# Func: read the differences from "difference.dat", and show
#       coverage differences as we wish.
#**********************************************************************

import pickle
import re

infile = open("difference.dat", "rb")
errorList = pickle.load(infile)
infile.close()

# Format: ErrorList: (ClassName, methodName): [(TestCase, version_pair[(1, 2, lineNumber), ]), ]

# just show some basic information, say what testcases distinguish a method.
newList = []
for item in errorList:
    value = errorList[item]
    caseList = []
    for item2 in value:
        if item2[0] not in caseList:
            caseList.append(item2[0])
    newList.append((item[0], item[1], caseList))


ignore_method_list = [] # (class, method)

ignore_class_reg = r"hohoho"
ignore_method_reg = r"hohoho"


for item in newList:
    if (item[0], item[1]) not in ignore_method_list and \
           len(re.findall(ignore_class_reg, item[0])) == 0 and \
           len(re.findall(ignore_method_reg, item[1])) == 0:

        print item[0] + '.' + item[1] + "():\t", item[2]

# print "errorList:"
# for item in errorList:
    # print '(', item, ':\n\t', errorList[item], ')'


