#!/usr/bin/python

# Compare file1 with file2, to see whether coverage 1 is in coverage 2.

import sys



absPathFlag = True

def find(dict, fileName, lines, obj, missFileList):
    if fileName not in dict:
        # print fileName, " not covered by the local tests."
        if fileName not in missFileList:
            missFileList.append(fileName)
        return True # already reported, so can go on

    for item in dict[fileName]:
        start, end = item

        for i in range(start, end):
            line = lines[i]
            if line.startswith(obj):
                if line.strip().split(',')[1] != '0':
                    # print line, i
                    return True
                else:
                    return False

    return False
            



missFileList = []
missLineList = []



infile1 = open(sys.argv[1], "r")
infile2 = open(sys.argv[2], "r")

lineList1 = infile1.readlines()
lineList2 = infile2.readlines()

# print len(lineList1)
# print len(lineList2)

# marks
fileName1 = ""
uncovCounter = 0
fileName2 = ""
start = 0
end = 0
# make a dictionary, using the file path as key, and (start,end) line as value
dictFile2 = {}
for i in range(0, len(lineList2)):
    line = lineList2[i].strip()
    if line.startswith("SF:"):
        fileName2 = line[3:].strip()
        if absPathFlag == False:
            fileName2 = fileName2.split('/')[-1]
        start = i
        continue
    elif line == "end_of_record":
        end = i
        if fileName2.endswith('.h'):
            start = 0
            end = 0
            continue

        if fileName2 not in dictFile2:
            dictFile2[fileName2] = [(start, end),]
            start = 0
            end = 0
            fileName2 = ''
        else:
            # print "hohoho"
            # print fileName2
            # exit()
            dictFile2[fileName2].append((start, end))
            start = 0
            end = 0
            fileName2 = ''


# for item in dictFile2:
    # print item
    # print dictFile2[item]
# exit()            

# later...
for i in range(0, len(lineList1)):
    line = lineList1[i]

    if line.strip() == "TN:":
        uncovCounter = 0
        continue
    elif line.strip().startswith('SF:'):
        fileName1 = line[3:].strip()
        if absPathFlag == False:
            fileName1 = fileName1.split('/')[-1]
        continue
    elif line.startswith("FN"):
        continue
    elif line.startswith("DA:"):
        if fileName1.endswith('.h'):
            continue
        line = line.strip()
        if line.split(',')[1] != '0':
            obj = line.split(',')[0]
            if find(dictFile2, fileName1, lineList2, obj, missFileList) == True:
                continue
            else:
                # print "Not found"
                # print fileName1, obj
                if (fileName1, obj) not in missLineList:
                    missLineList.append((fileName1, obj))
                continue

print "Misslinelist:"
for item in missLineList:
    print item



# print "MisslineList files:"

newList = []
for item in missLineList:
    if item[0] not in newList:
        newList.append(item[0])

print len(missLineList), "lines in ", len(newList), "files are covered."

# for item in newList:
    # print item

# print "Missfilelist:"
# for item in missFileList:
    # print item
print len(missFileList), "files are not covered at all."
