#!/usr/bin/python
########################################
#
# File: instrumental.py
# Author: Teng Long (tlong@cs.umd.edu)
# Description:
#   Automatically instrument the functions in the given list.
#
########################################


# Instrumental strategy:
#   From the given list, find the name and position of the function.
#   For each argument of the function, match its type, and add output right
#   after the '{' line

# instrumental -i input_file_of_functions -b base_directory -t typelist

import os
import re
import sys
import getopt


# get arguments
args = sys.argv[1:]
optlist, args = getopt.gnu_getopt(args, "i:b:t:")

# print optlist
# print args

basedir = None
inputFile = None # an input file as output of lcovPlus -f function
typelist = None # a file specify typename in the sourcefile and actual type

# if '-b' in [item[0] for item in optlist]:
for item in optlist:
    if item[0] == '-i':
        inputFile = item[1];
    elif item[0] == '-b':
        basedir = item[1]
    elif item[0] == '-t':
        typelist = item[1]

if typelist == None:
    print >> sys.stderr, "typelist must be specified"
    sys.exit(1)

if inputFile == None:
    print >> sys.stderr, "inputFile must be specified"
    sys.exit(1)

# print "base:", basedir
# print "input:", inputFile


#############################
#
# get function list in a dict format
#
#############################

fundict = {} # dictionary of {sourceFile: [funName]}

currentSourcePath = None

infileLines = open(inputFile, 'r').readlines()
for item in infileLines:
    item = item.strip()
    if item.startswith("FILE:"):
        currentSourcePath = item.split(':')[1].strip()
        if basedir != None:
            if basedir.endswith('/'):
                basedir = basedir[:-1]
            if currentSourcePath.startswith('/'):
                currentSourcePath = currentSourcePath[1:]
            currentSourcePath = basedir + '/' + currentSourcePath
        if currentSourcePath not in fundict:
            fundict[currentSourcePath] = []
        # print currentSourcePath
    else:
        funName = item.split(':')[0].strip()
        # print funName
        fundict[currentSourcePath].append(funName)



#############################
#
# files to look for
#
#############################

filelist = []

cmd1 = "find " + basedir + " -name '*.h'"
cmd2 = "find " + basedir + " -name '*.c'"

# print cmd1
# print cmd2

result1 = os.popen(cmd1).readlines()
for item in result1:
    filelist.append('./' + item.strip())
result2 = os.popen(cmd2).readlines()
for item in result2:
    filelist.append('./' + item.strip())

# for item in filelist:
#     print item

# exit()




##################
#
# typelist
#
##################

# typematch = {}

# for line in open(typelist, 'r').readlines():
#     line = line.strip()
#     if not line.startswith("#"):
#         typematch[line.split(':')[0].strip()] = line.split(':')[1].strip()

# print "typematch:"
# print typematch




##############################
#
# instrumenting
#
##############################

types = []
# write to exchange content file
exchfile = open("./exchange.txt", "w")


for idxsource in fundict:
    funcSet = fundict[idxsource]

    for func in funcSet: # find each function

        exchangeDir = {}
        
        for source in filelist:
            if not (source.endswith(".c") or source.endswith(".h")):
                continue
            # if source.endswith("fileacc.c"):
            #     print source
            with open(source) as fl_source:
                text_source = fl_source.read()

                # regexp = "^.*" + "[\*\s]+" + "(" + func + "[\s]*\(" +".*?\)).*$"
                # regexp = "^.*" + "[\*\s]+" + "(" + func + "[\s]*\(" +"[^;]*?\)\s*{).*$"            
                # regexp = "^.*" + "[\*\s]+" + "(" + func + "[\s]*\(" +"[^;\s]+?\s+[^;]+?" + "\)\s*{).*$"
                regexp = "^.*?" + "[\*\s]+" + "(" + func + "[\s]*\(" +"[^;\s]+?\s+[^;]+?" + "\)\s*{).*$"
                pattern = re.compile(regexp, re.DOTALL)
                result = pattern.findall(text_source)
            
                if len(result) > 1:
                    # print "\nsource:", source
                    # print "func:", func
                    print >> sys.stderr, "\nError, more than one appearance of function", func
                    for item in result:
                        print >> sys.stderr, item
                    sys.exit(1)
                elif len(result) == 1:
                    # print "\nExact one match in:", source
                    # print result
                    text = result[0]
                    ret = text.rfind("*/")
                    if ret != -1:
                        text = text[ret+2:]
                    if "if" not in text:
                        exchangeDir[source] = text
                    
                        
                # elif len(result) == 0:
                #     print "\nsource:", source
                #     print "func:", func
                #     print >> sys.stderr, "Error, no function was found", func
                #     sys.exit(1)
                
        for item in exchangeDir:
            # text = exchangeDir[item].replace('\n', '')
            text = exchangeDir[item]
            m = re.match(r".*\((.*)\)", text, re.DOTALL)
            if m:
                arguments = m.group(1)
                print '----------------------------------------------------------------------'
                print text
                pairs = arguments.split(',')
                for pair in pairs:
                    if '*' in pair:
                        continue
                    else:
                        datatype = ' '.join(pair.split()[:-1])
                        print datatype
                        types.append(datatype)
            else:
                print "shit"
                continue

        # if len(exchangeDir) != 1:
        #     print "idx source: ", idxsource
        #     print "func: ", func
        #     print len(exchangeDir)
        #     for item in exchangeDir:
        #         print item, ": ", (exchangeDir[item]).replace('\n', ' ')


        for item in exchangeDir:
            exchfile.write( "$" + item )
            exchfile.write( "@" + exchangeDir[item] )
            

# write to type file
typefile = open("./types.txt", "w")
types = list(set(types))
for item in types:
    print >> typefile, item
typefile.close()

exchfile.close()


# types = list(set(types))
# print len(types)
# for item in types:
#     print item

exit()



##############################
#
# instrumenting - obsolete
#
##############################


for source in fundict:
    funcSet = fundict[source]

    with open(source) as fl_source:
        text_source = fl_source.read()
        for func in funcSet:


            regexp = "^.*" + "[\*\s]+" + "(" + func + "[\s]*\(" +".*?\)).*$"
            
            pattern = re.compile(regexp, re.DOTALL)
            result = pattern.findall(text_source)
            
            if len(result) > 1:
                print "\nsource:", source
                print "func:", func
                print >> sys.stderr, "Error, more than one appearance of function", func
                for item in result:
                    print >> sys.stderr, item
                sys.exit(1)
            elif len(result) == 0:
                print "\nsource:", source
                print "func:", func
                print >> sys.stderr, "Error, no function was found", func
                sys.exit(1)



exit()






