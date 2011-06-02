#!/usr/bin/python

# Compare file1 with file2, to see whether coverage 1 is in coverage 2.


import sys

infile1 = open(sys.argv[1], "r")
infile2 = open(sys.argv[2], "r")

lineList1 = infile1.readlines()
lineList2 = infile2.readlines()


# make a dictionary of dictionaries. use the path as the key to find a
# dictionary, and in this dict, (BRDA: line, block, branch) will be
# the key, (hit) will be the value.

fileName2 = ""
dictFile2 = {}
tmpDict = None

for i in range(0, len(lineList2)):
    line = lineList2[i].strip()
    if line.startswith("SF:"):
        fileName2 = line[3:].strip()
        tmpDict = {}
    elif line == "end_of_record":
        if fileName2.endswith('.h'):
            continue
        else:
            dictFile2[fileName2] = tmpDict
    elif line.startswith('BRDA:'):
        quad = line[5:].split(',')
        # print quad
        key = (quad[0], quad[1], quad[2])
        tmpDict[key] = quad[3]

# for item in  dictFile2:
    # print item, ':\n', dictFile2[item]


records = []

fileName1 = ""
isHeader = False
missFile = []
for i in range(0, len(lineList1)):
    line = lineList1[i].strip()
    if line.startswith("SF:"):
        fileName1 = line[3:].strip()
        if fileName1.endswith('.h'):
            isHeader = True
        else:
            isHeader = False
    elif line.startswith('BRDA:'):
        if isHeader == True:
            continue
        quad = line[5:].split(',')
        key = (quad[0], quad[1], quad[2])
        value = quad[3]
        if fileName1 not in dictFile2:
            if fileName1 not in missFile:
                missFile.append(fileName1)
            continue

        if dictFile2[fileName1][key] != value:
            
            original = dictFile2[fileName1][key]
            new = value
            if (original == '0' or original == '-') and (new != '0' and new !='-'):
                rec = (fileName1, key, original, new)
                records.append(rec)

for item in records:
    print item

print len(records)

fileList = []
for item in records:
    if item[0] not in fileList:
        fileList.append(item[0])

print "files that have missed branch:"
for item in fileList:
    print item

print len(fileList)    

print "missing files:"
for item in missFile:
    print item
