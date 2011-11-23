#!/usr/bin/python

########################################
#
# File: patch.py
# Author: Teng Long (tlong@cs.umd.edu)
# Description:
#   Automatically instrument the functions according to the exchange list
#   and the type list
#
########################################



# patch.py -e exchange.txt -t typelist
# exchange.txt: exchange list that has the path to the sources that needs to be
#   instrumented, and the text to be replaced.
# typelist: match self-defined types to standard types.

import os
import re
import sys
import getopt


# get arguments
args = sys.argv[1:]
optlist, args = getopt.gnu_getopt(args, "e:t:")

# print optlist
# print args

exchangeFile = None 
typelist = None 


for item in optlist:
    if item[0] == '-e':
        exchangeFile = item[1];
    elif item[0] == '-t':
        typelist = item[1]

if typelist == None:
    print >> sys.stderr, "typelist must be specified"
    sys.exit(1)

if exchangeFile == None:
    print >> sys.stderr, "exchangeFile must be specified"
    sys.exit(1)

########################
# read the type list
########################

types_fd = open(typelist)
typeDict = {}
for item in types_fd.readlines():
    if len(item.strip()) == 0:
        continue
    item = item.strip().split(":")
    if item[0].strip() not in typeDict:
        typeDict[item[0].strip()] = item[1].strip()
    else:
        if typeDict[item[0]] != item[1].strip():
            print "item[0]:", item[0], "item[1]", item[1], "old:", typeDict[item[0]]
            print "shit 1!!"
            exit()
# print "we are good"
# print len(typeDict)
# for item in typeDict:
#     print item, ":", typeDict[item]
# exit()

########################
# read exchange list
########################


exchange_file_content = open(exchangeFile, 'r').read()
tmpList = exchange_file_content.split('$')
exchangeList = []
for item in tmpList:
    exchangeList.append(item.split('@'))

for pair in exchangeList:
    if len(pair) != 2:
        continue
    source = pair[0]
    text = pair[1]
    source_fd = open(source)
    content = source_fd.read()
    source_fd.close()    

    if text not in content:
        print "source:"
        print source
        print "text:"
        print text
        # print "content:"
        # print content
        print "shit 2!"
        exit()
    else:
        # print "bingo"

        # add include file
        include_info = '#ifndef _TEST_INST_H\n#include "testinst.h"\n#endif\n'
        if not content.startswith(include_info):
            content = include_info + content


        # process the text, append output information
        reg = r"(.*)\((.*)\)"
        m = re.match(reg, text, re.DOTALL)
        if m:
            arguments = m.group(2)
            print '----------------------------------------------------------------------'
            print text
            argpairs = arguments.split(',')

            inst_lines = "\n"
            funName = m.group(1).split()[-1].strip()
            
            for pair in argpairs:
                if '*' in pair:
                    continue
                elif '[' in pair: # int haha[]
                    continue
                else:
                    datatype = ' '.join(pair.split()[:-1])
                    argName = pair.split()[-1].strip()
                    if datatype.startswith("register"):
                        datatype = datatype.replace("register", "").strip()
                    if datatype.startswith("const"):
                        datatype = datatype.replace("const", "").strip()                        
                    if datatype not in typeDict:
                        continue
                    mapedType = typeDict[datatype]

                    
                    
                    print "datatype:", datatype
                    print "mappedtype:", mapedType
                    print "fun name:", funName
                    print "arg name:", argName

                    control_bit = '' # the only difference of instrumented functions. The instout_* '*' part.
                    if mapedType == "int":
                        control_bit = "i"
                    elif mapedType == "unsigned":
                        control_bit = "u"
                    elif mapedType == "signed":
                        control_bit = "i"
                    elif mapedType == "double":
                        control_bit = "d"
                    elif mapedType == "long":
                        control_bit = "l"
                    elif mapedType == "long long":
                        control_bit = "ll"
                    elif mapedType == "unsigned long":
                        control_bit = "lu"
                    else:
                        print >> sys.stderr, "Error, no instrumentation function available for this kind of mapped data type. Please check."
                        sys.exit(1)
                        
                    callString = "instout_" + control_bit + '("' + funName + '", "' + argName + '", ' + argName + ");\n"
                    inst_lines += callString
                        
        # print "inst lines:"
        # print inst_lines
        if inst_lines not in content:
            content = content.replace(text, text + inst_lines)

        # write back to file
        source_fd = open(source, 'w')
        source_fd.write(content)
        source_fd.close()
        
        
        

    source_fd.close()
    
