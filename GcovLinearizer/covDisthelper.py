########################################
#
# File: covDisthelper.py
# Description:
#   Functions for covDist.py
#
########################################


import sys
import os


########################################
#
# Definitions:
# 1. File coverage:
#    [(souceFilename, #total, #hit, coveredPercentage), ...]
#
########################################

def fileCovL(covDictL): # covDictL: {sourceFile, {line#, hit_times}} }
    result = []
    srcList = covDictL.keys()
    srcList.sort()
    for item in srcList:
        if "/test/" in item:
            continue
        covStat = covDictL[item]
        numLine = len(covStat) # total # of lines of that src file.
        hitCount = 0
        for sItem in covStat:
            if covStat[sItem] != 0:
                hitCount += 1
        hitRate = float(hitCount) / float(numLine)
        
        result.append((item, numLine, hitCount, hitRate))

    return result

def fileCovB(covDictB):# covDictB: {srcFile, {(line#, block#, br#), hit_times}}
    result = []
    srcList = covDictB.keys()
    srcList.sort()
    for item in srcList:
        if "/test/" in item:
            continue
        covStat = covDictB[item]
        numBr = len(covStat) # total number of branches of that src file
        if numBr == 0: # no branches
            continue
        else:
            hitCount = 0
            for sItem in covStat:
                if covStat[sItem] != 0:
                    hitCount += 1
            hitRate = float(hitCount) / float(numBr)
            result.append((item, numBr, hitCount, hitRate))

    return result


def homeDir(pathList):
    commonprefix = os.path.commonprefix(pathList)
    if commonprefix.endswith('/'):
        return commonprefix
    else:
        parts = commonprefix.split('/')
        commonprefix = '/'.join(parts[:-1])
        commonprefix += '/'
        return commonprefix

# covList is in form of [(item, totalNum, numHit, hitRate), ...]
#  scale: how many subdirectories to go into from the home directory of the src
def zoom(covList, zoomScale):
    allPaths = []
    for item in covList:
        allPaths.append(item[0])
        # print item[0]
    home = homeDir(allPaths)

    splitHome = home.split('/')
    # print "splitHome:", splitHome

    homeLen = len(splitHome)

    tmpList = []

    for item in covList:
        path = item[0].split('/')

        relaPath = path[homeLen - 1:]

        # print "path:", path
        # print "relaPath:", relaPath

        if len(relaPath) < zoomScale + 1:
            print >> sys.stderr, "Error, over zoomed in."
            print >> sys.stderr, "relative path:", relaPath
            print >> sys.stderr, "zoom scale:", zoomScale
            sys.exit(1)

        tmpList.append((relaPath, item[1], item[2], item[3]))

    totalNum = 0
    hitNum = 0

    flag = False # the first item in tmpList
    curDir = None
    result = []
    
    counter = 0
    
    for item in tmpList:
        counter += 1
        relaPath = item[0]
        if flag == False:
            curDir = relaPath[0:zoomScale]
            totalNum = item[1]
            hitNum = item[2]
            if counter == len(tmpList): # all items are processed
                result.append(('/'.join(curDir), totalNum, hitNum, float(hitNum) / float(totalNum)))
            flag = True
            continue
        else:
            if relaPath[0:zoomScale] == curDir:
                # print "cumulating..."
                totalNum += item[1]
                hitNum += item[2]
                if counter == len(tmpList): # all items are processed
                    print "totalNum:", totalNum, "hitNum:", hitNum
                    result.append(('/'.join(curDir), totalNum, hitNum, float(hitNum) / float(totalNum)))
                continue
            else:
                result.append(('/'.join(curDir), totalNum, hitNum, float(hitNum) / float(totalNum)))
                curDir = relaPath[0:zoomScale]
                totalNum = item[1]
                hitNum = item[2]
                continue
    return result

def covDictAndL(dict1, dict2):

    result = {}
    for item in dict1.keys():
        result[item] = {}
        lines = dict1[item]

        for line in lines:
            if lines[line] != 0 and \
               item in dict2 and \
               line in dict2[item] and \
               dict2[item][line] != 0:
                result[item][line] = 1
            else:
                result[item][line] = 0
    return result

def covDictOrL(dict1, dict2):

    result = {}
    for item in dict1.keys():
        result[item] = {}
        lines = dict1[item]

        for line in lines:
            if lines[line] == 0 and \
               (item not in dict2 or \
                line not in dict2[item] or \
                dict2[item][line] == 0):
                result[item][line] = 0
            else:
                result[item][line] = 1
    return result
            

def covDictExtraL(dict1, dict2):

    result = {}
    for item in dict1.keys():
        result[item] = {}
        lines = dict1[item]
        
        for line in lines:
            if lines[line] != 0 and \
                   (item not in dict2 or \
                    line not in dict2[item] or \
                    dict2[item][line] == 0):
                result[item][line] = 1
            else:
                result[item][line] = 0
    return result


def covDictAndB(dict1, dict2):

    result = {}
    for item in dict1.keys():
        result[item] = {}
        brs = dict1[item]

        for branch in brs:
            if brs[branch] != 0 and \
               item in dict2 and \
               branch in dict2[item] and \
               dict2[item][branch] != 0:
                result[item][branch] = 1
            else:
                result[item][branch] = 0
    return result

def covDictOrB(dict1, dict2):

    result = {}
    for item in dict1.keys():
        result[item] = {}
        brs = dict1[item]

        for branch in brs:
            if brs[branch] == 0 and \
               (item not in dict2 or \
                branch not in dict2[item] or \
                dict2[item][branch] == 0):
                result[item][branch] = 0
            else:
                result[item][branch] = 1
    return result


def covDictExtraB(dict1, dict2):

    result = {}
    for item in dict1.keys():
        result[item] = {}
        brs = dict1[item]

        for branch in brs:
            # if (item not in dict2) or \
            #    (line not in dict2[item]) or \
            #        (lines[line] != 0 and dict2[item][line] == 0):
            #     result[item][line] = 1

            if brs[branch] != 0 and \
               (item not in dict2 or \
                branch not in dict2[item] or \
                dict2[item][branch] == 0):
                result[item][branch] = 1
            else:
                result[item][branch] = 0
    return result

