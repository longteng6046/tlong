##################################################
#
# File: ignoreList.py
# Description:
#   Scan the coverage data dictionary file generated for different rous on
#    the same configuration, find out classes that have different coveage,
#    and mark them out in an ignore list.
#
##################################################

import pickle
import sys

if len(sys.argv) != 2:
    print "Error! Format: python ignoreList.py PATH/TO/.DIC/FILE"
    sys.exit(1)

########################################
# Load data
########################################


print "... beginning to load data ..."    
infile = open(sys.argv[1], 'rb')
covDict = pickle.load(infile)
print "finished data loading!"
print "There are ", len(covDict), "test cases in the data file."




########################################
# Get a sample from the dict, create class file list
########################################

classList = [] # format: [(pkgname, className), ]

for item in covDict:
    for sItem in covDict[item]:
        dataDict = covDict[item][sItem]
        for pkg in dataDict.keys():
            for cls in dataDict[pkg].keys():
                classList.append((pkg, cls))
        break
    break

print "# of class:", len(classList)
# print "# of class:", len(set(classList))
# exit()
        


########################################
# Build the ignore list
########################################

ignoreList = []
ignoreDict = {}


counter = 0
for item in covDict: # for each test case
    counter += 1
    cfgDict =  covDict[item] # dict of different convigures
    keys = cfgDict.keys()
    for i in range(0, len(keys)):
        for j in range(i + 1, len(keys)):
            dataDict1 = cfgDict[keys[i]]
            dataDict2 = cfgDict[keys[j]]

            for k in classList:
                pkg = k[0]
                cls = k[1]
                try:
                    if dataDict1[pkg][cls] != dataDict2[pkg][cls]:
                        ignoreList.append(k)
                except:
                    print "Exception happened!!!!!!!!!"
                    print "test:", item
                    print "keys[i]:", keys[i], "keys[j]:", keys[j]
                    print dataDict1.keys()
                    print dataDict2.keys()
                    continue
print "ignoreList length:", len(ignoreList)
print "ignoreList set length:", len(set(ignoreList))
# for item in set(ignoreList):
    # print item


##############################
# Save the ignore list to a file.
##############################

print "Begin to save ignore list to the dictionary..."

covDictFile = open("ignore.list", 'w')
pickle.dump(list(set(ignoreList)), covDictFile)
covDictFile.close()

print "Finished saving."
