#!/usr/bin/python
# ******************************************************************************
#
# Filter: filter any testcases that cause a "ComponentNotFound" or
#         "ComponentDisabled" Exception.
# ******************************************************************************

import os
import sys
import time
import random

# Check command format


if len(sys.argv) != 4 and len(sys.argv) != 6:
    print "Format: ./filter.py log_dir testcase_dir dest_testcase_dir [report_dir dest_report_dir]"
    sys.exit(1)

log_dir = os.path.abspath(sys.argv[1])
tc_dir = os.path.abspath(sys.argv[2])
dest_tc_dir = os.path.abspath(sys.argv[3])
cmd = "rm -rf " + dest_tc_dir + "/*"

os.system(cmd)


if len(sys.argv) == 6:
    report_dir = os.path.abspath(sys.argv[4])
    dest_report_dir = os.path.abspath(sys.argv[5])
    cmd = "rm -rf " + dest_report_dir + "/*"    
    os.system(cmd)


# get all log filenames
tmp = os.popen('ls ' + sys.argv[1]).readlines()
print "Path: " + sys.argv[1]
if len(tmp) == 0:
    print "File not found."
    print "error"
    exit()

base = os.path.abspath(sys.argv[1])

# process logs, try to find those exceptions
count = 0
maximum = 500
random.shuffle(tmp)

for item in tmp:
    fileName = item.strip()
    print fileName


    # look for normal termination
    cmd = "cat " + base + "/" + fileName + " | grep 'NORMALLY TERMINATED'"
    result = os.popen(cmd).readlines() 

    # process the ones that didn't terminate properly
    if len(result) == 1:
        count += 1
        if count > maximum:
            break

        # process
        objName = item[:-13]

        cmd = "cp -r " +  tc_dir + "/" + objName + " " + dest_tc_dir
        os.system(cmd)

        if len(sys.argv) == 6:
            cmd = "cp -r " + report_dir + "/" + objName + " " + dest_report_dir + '/'
            os.system(cmd)

