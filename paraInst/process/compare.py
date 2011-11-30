#!/usr/bin/python

list = ['self.txt', 'petsc.txt', 'tao.txt', 'slepc.txt', 'together_l2.txt']

funDir = {}

funDir = {}

for file in list:

    fd = open(file)
    lines = fd.readlines()

    for line in lines:
        if ':' not in line:
            continue

        funName = line.split(':')[0].strip()
        scale = line.split(':')[1].strip()

        if funName not in funDir:
            funDir[funName] = {}
            funDir[funName][file] = scale
        else:
            funDir[funName][file] = scale
    

resultDir = {}


ctr = 0
for funName in funDir:
    # print item, funDir[item]

    subDir = funDir[funName]

    if "self.txt" not in subDir:
        # print subDir
        continue
    

    # (low_bound, high_bound) = subDir["self.txt"]

    low_bound = subDir["self.txt"].strip()[1:-1].split(',')[0]
    if '.' in low_bound:
        low_bound = float(low_bound)
    else:
        low_bound = int(low_bound)
    high_bound = subDir["self.txt"].strip()[1:-1].split(',')[1]

    if '.' in high_bound:
        high_bound = float(high_bound)
    else:
        high_bound = int(high_bound)
    # print low_bound, high_bound

    flag = False

    for item in subDir:
        if item != "self.txt":
            low = subDir[item].strip()[1:-1].split(',')[0]
            if '.' in low:
                low = float(low)
            else:
                low = int (low)
                
            high = subDir[item].strip()[1:-1].split(',')[1]
            if '.' in high:
                high = float(high)
            else:
                high = int(high)
            # print low, high
            if low < low_bound or high > high_bound:
                flag = True
                print item, "(", low, ",", high, ")"
    if flag == True:
        print "self: (", low_bound, ",", high_bound, ")"
        print funName
        ctr += 1
        print ctr
        print "--------------------------------------------------------------------------------"
