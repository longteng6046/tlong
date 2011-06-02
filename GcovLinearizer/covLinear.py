##############################
#
# File: covLinear.py
# Function: linearlize and compare the coverage of the same package.
#
##############################

import sys
import os


##############################
#
# Coverage data read
#
##############################


# Step 1: get the .info file list.

if len(sys.argv) != 2:
    print "Error: Format: python covLinear.py DIR/TO/.INFO/FILES"
    sys.exit(1)

fileDir = os.path.abspath(sys.argv[1])

# print "file path: ", fileDir

infoList = []

for item in os.listdir(fileDir):
    if ".info" in item and not "~" in item and not "#" in item:
        item = fileDir + '/' + item
        infoList.append(item)

infoList.sort()

contentList = {}
for item in infoList:
    # print item
    contentList[item] = open(item, 'r')

# print contentList

# Step 2: scan .info files, store coverage data
# Coverage data:
#  lineCovData = { fileName, {sourceFile, {line#, hit_times}} }
#  funCovData = { fileName, {sourceFile, {func_name, hit_times}} }
#  brCovData = { fileName, {sourceFile, {(line#, block#, br#), hit_times}} }
#  
# Summary data:
# key: 'found', 'hit'; val: int
#  lineSum = {fileName, {sourceFile, {key, val}}}
#  funSum = {fileName, {sourceFile, {key, val}}}
#  brSum = {fileName, {sourceFile, {key, val}}}


lineCovData = {}
funCovData = {}
brCovData = {}

lineSum = {}
funSum = {}
brSum = {}

for item in contentList:

    if item not in lineCovData:
        lineCovData[item] = {}
        funCovData[item] = {}
        brCovData[item] = {}

        lineSum[item] = {}
        funSum[item] = {}
        brSum[item] = {}
    content = contentList[item].readlines()


    # status flags for each file
    sourceFile = '' # the abspath to the source file
    isCFile = False # indicating whether it is a .c file


    # for each file
    for line in content:

        line = line.strip()

        if line.startswith('SF:'):
            sourceFile = line[3:]
            if sourceFile.endswith('.c'):
                isCFile = True
                if sourceFile not in lineCovData[item]:
                    lineCovData[item][sourceFile] = {}
                    funCovData[item][sourceFile] = {}
                    brCovData[item][sourceFile] = {}

                    lineSum[item][sourceFile] = {}
                    funSum[item][sourceFile] = {}
                    brSum[item][sourceFile] = {}
                else:
                    print "Error: duplicated source file:"
                    print "Filename: ", item
                    print "Source file name: ", source
                    sys.exit(1)

            elif sourceFile.endswith('.h'):
                isCFile = False
                continue
            else:
                print "Error: wired filename..."
                sys.exit(1)

        # if it is currently a '.h' file, then skip the current line
        elif isCFile == False:
            continue

        elif line.startswith('FN:'):
            funName = line.split(',')[1]
            # print funName
            # print line
            funCovData[item][sourceFile][funName] = None
            continue
        
        elif line.startswith('FNDA:'):
            funName = line.split(',')[1]
            hitTimes = line.split(',')[0].split(':')[1]
            if funCovData[item][sourceFile][funName] == None:
                funCovData[item][sourceFile][funName] = int(hitTimes)
            else:
                print "Error: muliple function hit record."
                print "file: ", item
                print "source file: ", sourceFile
                print "function name: ", funName
                sys.exit(1)
            continue

        elif line.startswith('FNF:'):
            funSum[item][sourceFile]['found'] = int(line[4:])
            continue

        elif line.startswith('FNH:'):
            # print int(line[4:])
            funSum[item][sourceFile]['hit'] = int(line[4:])

        elif line.startswith('BRDA:'):
            data = line[5:].split(',')
            key = (data[0], data[1], data[2])
            if data[3] == '-':
                val = 0
            else:
                val = int(data[3])
            brCovData[item][sourceFile][key] = val
            continue

        elif line.startswith('BRF:'):
            brSum[item][sourceFile]['found'] = int(line[4:])
            continue

        elif line.startswith('BRH:'):
            brSum[item][sourceFile]['hit'] = int(line[4:])
            # print int(line[4:])
            continue
            
        elif line.startswith('DA:'):
            data = line[3:]
            line_num = data.split(',')[0]
            hit_num = int(data.split(',')[1])
            lineCovData[item][sourceFile][line_num] = hit_num
            continue

        elif line.startswith('LF:'):
            lineSum[item][sourceFile]['found'] = int(line[3:])
            continue

        elif line.startswith('LH:'):
            lineSum[item][sourceFile]['hit'] = int(line[3:])
            # print item, sourceFile
            # print int(line[3:])
            # print lineSum[item][sourceFile]
            continue

        else:
            continue



##############################
#
# Coverage Statistics
#
##############################


# lineStat_single = {(sourcefile, line#), isHit}
# funStat_single = {(sourcefile, func_name, isHit)}
# brStat_single = {(sourcefile, line#, block#, br#), isHit}

# lineStat = {(sourcefile, line#), hitTimes}
# funStat = {(sourcefile, func_name, hitTimes)}
# brStat = {(sourcefile, line#, block#, br#), hitTimes}

# CAUTION: we DO NOT count apr's own unit test in coverage statistics


lineStat_single = {}
funStat_single = {}
brStat_single = {}

lineStat = {}
funStat = {}
brStat = {}

for item in lineCovData.keys():
    print item

sourceList = lineCovData['/home/tlong/Dropbox/repository/coverage_linearize/files/httpd_flood.info']


# print infoList

for item in sourceList:
    for sItem in sourceList[item]:
        key = (item, sItem)
        # print key
        val = 0
        counter = 0
        for infoFile in infoList:
            if 'self' not in infoFile:
                # print "infoFile", infoFile
                if sItem not in lineCovData[infoFile][item]:
                    continue
                val += lineCovData[infoFile][item][sItem]
                if lineCovData[infoFile][item][sItem] != 0:
                    counter += 1

        # print (key, val)
        lineStat[key] = val
        lineStat_single[key] = counter

sourceList = funCovData['/home/tlong/Dropbox/repository/coverage_linearize/files/httpd_flood.info']

for item in sourceList:
    for sItem in sourceList[item]:
        key = (item, sItem)
        val = 0
        counter = 0

        for infoFile in infoList:
            if 'self' not in infoFile:
                # print "infoFile", infoFile
                val += funCovData[infoFile][item][sItem]
                if funCovData[infoFile][item][sItem] != 0:
                    counter += 1
        
        funStat[key] = val
        funStat_single[key] = counter
        # if val == 0:
        #     funStat_single[key] = 0
        # else:
        #     funStat_single[key] = 1


sourceList = brCovData['/home/tlong/Dropbox/repository/coverage_linearize/files/httpd_flood.info']

for item in sourceList:
    for sItem in sourceList[item]:
        key = (item, sItem)
        val = 0
        counter = 0

        for infoFile in infoList:
            if 'self' not in infoFile:
                # print "infoFile", infoFile
                if sItem not in brCovData[infoFile][item]:
                    continue
                val += brCovData[infoFile][item][sItem]
                if brCovData[infoFile][item][sItem] != 0:
                    counter += 1
                
        brStat[key] = val
        brStat_single[key] = counter






########################################
#
# Data analysis part
#
########################################

# Questions to answer:
# 0. What is the statistics of the apr package?
# 1. What is the coverage of the unit test of apr?
# 2. What is the coverage brought to apr by each individual upper-level package?
# 3. What is the extra coverage brought to apr by each individual upper-leve package?
# 4. What is the overall coverage brought to apr by the 4 upper-level packages?
# 5. What is the extra coverage brought to apr by all upper-level packages together?
# 6. What is the overlap of coverage from the 4 upper-level packages?
# 7. What is the overlap of the 4 upper-level packages' extra coverage?



print r'''
##############################
#
# 0. What is the statistics of the apr package?
#
##############################
'''

totalLine = len(lineStat)
totalFun = len(funStat)
totalBr = len(brStat)

print "Number of lines: ", totalLine
print "Number of functions: ", totalFun
print "Number of branches: ", totalBr



print r'''
##############################
#
# 1. What is the coverage of the unit test of apr?
#
##############################
'''

unitName = '/home/tlong/Dropbox/repository/coverage_linearize/files/z_self.info'



subLineCov = lineCovData[unitName]
counter = 0
for item in subLineCov:
    for sItem in subLineCov[item]:
        if (item, sItem) in lineStat and \
               subLineCov[item][sItem] != 0:
            counter += 1


print "line_cov:", str(float(counter) / float(totalLine) * 100) + '%'

subFunCov = funCovData[unitName]
counter = 0
for item in subLineCov:
    for sItem in subFunCov[item]:
        if (item, sItem) in funStat and \
               subFunCov[item][sItem] != 0:
            counter += 1


print "fun_cov:", str(float(counter) / float(totalFun) * 100) + '%'

subBrCov = brCovData[unitName]
counter = 0
for item in subBrCov:
    for sItem in subBrCov[item]:
        if (item, sItem) in brStat and \
               subBrCov[item][sItem] != 0:
            counter += 1

print "br_cov:",  str(float(counter) / float(totalBr) * 100) + '%'


print r'''
##############################
#
# 2. What is the coverage brought to apr by each individual upper-level package?
#
##############################
'''



print "line_cov:"
sum = 0.0
for item in infoList:
    if 'self' not in item:
        # print item
        counter = 0
        for sItem in lineCovData[item]:
            # print sItem
            for ssItem in lineCovData[item][sItem]:
                # print ssItem
                # print lineCovData[item][sItem][ssItem]
                if lineCovData[item][sItem][ssItem] != 0:
                    counter += 1
        fileName = item.split('/')[-1].split('.')[0]
        print fileName, ':', str(float(counter) / float(totalLine) * 100) + '%'
        sum += float(counter) / float(totalLine)
print "\tSum: ", str(sum * 100) + '%'

print "\nfun_cov:"
sum = 0.0
for item in infoList:
    if 'self' not in item:
        # print item
        counter = 0
        for sItem in funCovData[item]:
            # print sItem
            for ssItem in funCovData[item][sItem]:
                # print ssItem
                # print lineCovData[item][sItem][ssItem]
                if funCovData[item][sItem][ssItem] != 0:
                    counter += 1
        fileName = item.split('/')[-1].split('.')[0]
        print fileName, ':', str(float(counter) / float(totalFun) * 100) + '%'
        sum += float(counter) / float(totalFun)
print "\tSum: ", str(sum * 100) + '%'        

print "\nbr_cov:"
sum = 0.0
for item in infoList:
    if 'self' not in item:
        # print item
        counter = 0
        for sItem in brCovData[item]:
            # print sItem
            for ssItem in brCovData[item][sItem]:
                # print ssItem
                # print lineCovData[item][sItem][ssItem]
                if brCovData[item][sItem][ssItem] != 0:
                    counter += 1
        fileName = item.split('/')[-1].split('.')[0]
        print fileName, ':', str(float(counter) / float(totalBr) * 100) + '%'
        sum += float(counter) / float(totalBr)
print "\tSum: ", str(sum * 100) + '%'        

print r'''
##############################
#
# 3. What is the extra coverage brought to apr by each individual upper-leve package?
#
##############################
'''

print "line_cov:"
sum = 0.0
for item in infoList:
    if 'self' not in item:
        counter = 0
        for sItem in lineCovData[item]:
            for ssItem in lineCovData[item][sItem]:
                if lineCovData[item][sItem][ssItem] != 0 and \
                       (lineCovData[unitName][sItem][ssItem] == 0 or \
                        ssItem not in lineCovData[unitName][sItem]):
                    counter += 1
        fileName = item.split('/')[-1].split('.')[0]
        print fileName, ':', str(float(counter) / float(totalLine) * 100) + '%'
        sum += float(counter) / float(totalLine)
print "\tSum: ", str(sum * 100) + '%'        
        
print "\nfun_cov:"
sum = 0.0
for item in infoList:
    if 'self' not in item:
        counter = 0
        for sItem in funCovData[item]:
            for ssItem in funCovData[item][sItem]:
                if funCovData[item][sItem][ssItem] != 0 and \
                       (funCovData[unitName][sItem][ssItem] == 0 or \
                        ssItem not in funCovData[unitName][sItem]):
                    counter += 1
        fileName = item.split('/')[-1].split('.')[0]
        print fileName, ':', str(float(counter) / float(totalFun) * 100) + '%'
        sum += float(counter) / float(totalFun)
print "\tSum: ", str(sum * 100) + '%'        

print "\nbr_cov:"
sum = 0.0
for item in infoList:
    if 'self' not in item:
        counter = 0
        for sItem in brCovData[item]:
            for ssItem in brCovData[item][sItem]:
                if brCovData[item][sItem][ssItem] != 0 and \
                       (brCovData[unitName][sItem][ssItem] == 0 or \
                        ssItem not in brCovData[unitName][sItem]):
                    counter += 1
        fileName = item.split('/')[-1].split('.')[0]
        print fileName, ':', str(float(counter) / float(totalBr) * 100) + '%'
        sum += float(counter) / float(totalBr)

print "\tSum: ", str(sum * 100) + '%'        


print r'''
##############################
#
# 4. What is the overall coverage brought to apr by the 4 upper-level packages?
#
##############################
'''

counter = 0
for item in lineStat:
    if lineStat[item] != 0:
        counter += 1
print "line_cov:", str(float(counter) / float(totalLine) * 100) + '%'

counter = 0
for item in funStat:
    if funStat[item] != 0:
        counter += 1
print "fun_cov:", str(float(counter) / float(totalFun) * 100) + '%'

counter = 0
for item in brStat:
    if brStat[item] != 0:
        counter += 1
print "br_cov:", str(float(counter) / float(totalBr) * 100) + '%'


print r'''
##############################
#
# 5. What is the extra coverage brought to apr by all upper-level packages together?
#
##############################
'''

counter = 0
for item in lineStat:
    if lineStat[item] != 0 and \
           lineCovData[unitName][item[0]][item[1]] == 0:
        counter += 1
print "line_cov:", str(float(counter) / float(totalLine) * 100) + '%'

counter = 0
for item in funStat:
    if funStat[item] != 0 and \
           funCovData[unitName][item[0]][item[1]] == 0:
        counter += 1
print "fun_cov:", str(float(counter) / float(totalFun) * 100) + '%'

counter = 0
for item in brStat:
    if brStat[item] != 0 and \
           brCovData[unitName][item[0]][item[1]] == 0:
        counter += 1
print "br_cov:", str(float(counter) / float(totalBr) * 100) + '%'


print r'''
##############################
#
# 6. What is the overlap of coverage from the 4 upper-level packages?
#
##############################
'''

for i in range(0, len(infoList)):
    counter = 0
    for item in lineStat_single:
        if lineStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalLine)
    print str(cov * 100) + '%', "lines are covered by", i, "packages."

print ''
for i in range(0, len(infoList)):
    counter = 0
    for item in funStat_single:
        if funStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalFun)
    print str(cov * 100) + '%', "functions are covered by", i, "packages."


print ''
for i in range(0, len(infoList)):
    counter = 0
    for item in brStat_single:
        if brStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalBr)
    print str(cov * 100) + '%', "branches are covered by", i, "packages."


print r'''
##############################
#
# 6. What is the overlap of coverage from the 4 upper-level packages?
#
##############################
'''

for i in range(0, len(infoList)):
    counter = 0
    for item in lineStat_single:
        if lineStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalLine)
    print str(cov * 100) + '%', "lines are covered by", i, "packages."

print ''
for i in range(0, len(infoList)):
    counter = 0
    for item in funStat_single:
        if funStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalFun)
    print str(cov * 100) + '%', "functions are covered by", i, "packages."


print ''
for i in range(0, len(infoList)):
    counter = 0
    for item in brStat_single:
        if brStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalBr)
    print str(cov * 100) + '%', "branches are covered by", i, "packages."


print r'''
##############################
#
# 6. What is the overlap of coverage from the 4 upper-level packages?
#
##############################
'''

for i in range(0, len(infoList)):
    counter = 0
    for item in lineStat_single:
        if lineStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalLine)
    print str(cov * 100) + '%', "lines are covered by", i, "packages."

print ''
for i in range(0, len(infoList)):
    counter = 0
    for item in funStat_single:
        if funStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalFun)
    print str(cov * 100) + '%', "functions are covered by", i, "packages."


print ''
for i in range(0, len(infoList)):
    counter = 0
    for item in brStat_single:
        if brStat_single[item] == i:
            counter += 1
    cov = float(counter) / float(totalBr)
    print str(cov * 100) + '%', "branches are covered by", i, "packages."




print r'''
##############################
#
# 7. What is the overlap of the extra coverage from the 4 upper-level packages?
#
##############################
'''

for i in range(0, len(infoList)):
    counter = 0
    for item in lineStat_single:
        if lineStat_single[item] == i and \
               lineCovData[unitName][item[0]][item[1]] == 0:
            counter += 1
    cov = float(counter) / float(totalLine)
    print str(cov * 100) + '%', "lines are covered by", i, "packages."

print ''
for i in range(0, len(infoList)):
    counter = 0
    for item in funStat_single:
        if funStat_single[item] == i and \
               funCovData[unitName][item[0]][item[1]] == 0:
            counter += 1
    cov = float(counter) / float(totalFun)
    print str(cov * 100) + '%', "functions are covered by", i, "packages."


print ''
for i in range(0, len(infoList)):
    counter = 0
    for item in brStat_single:
        if brStat_single[item] == i and \
               brCovData[unitName][item[0]][item[1]] == 0:
            counter += 1
    cov = float(counter) / float(totalBr)
    print str(cov * 100) + '%', "branches are covered by", i, "packages."


