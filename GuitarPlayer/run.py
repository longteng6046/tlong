#!/usr/bin/python

import os
import sys


# To run the testcase automatically in the given directory

# check whether te given original file exists

if len(sys.argv) != 2:
    print "Format: ./run.py test_case_list\n"
    exit()

tmp = os.popen('ls ' + sys.argv[1]).readlines()

if len(tmp) == 0 :
    print "File not found."
    print "error"
    exit()

for item in tmp:
    if item in tmp:
        if cmp(item.strip(), sys.argv[1]) != 0 :
            print "File not found.\n"
            print "error\n"
            exit()
    


# read test cases, one by one
cases = open(sys.argv[1]).readlines()[0]
cases = cases.replace(r',','\n')

# root dir
rootdir = "rundir"
tmpfile = open(rootdir+"/tmpCases.tmp",'w')
tmpfile.write(cases)
tmpfile.close()
cases = open(rootdir+"/tmpCases.tmp").readlines()

# make dir for all 

 # directory to store single property files

propdir = "rundir/properties/"
os.system("rm -rf " + propdir)
os.system("mkdir -p " + propdir)
 # directory for all .ser files
os.system("rm -rf rundir/sers/")
os.system("mkdir -p rundir/sers/")
 # directory for all reports
os.system("rm -rf rundir/reports")
os.system("mkdir -p rundir/reports/")

#get all testcases, for each case, run the replayer

#remove top-level existing .ser file
os.system("rm -rf cobertura.ser")

counter = 0

for casename in cases:
    counter += 1

    propName = "./rundir/properties/" + casename.strip() + ".properties"
    baseProp = open("./rundir/base.properties")
    newProp = open(propName, 'w')
    
    for line in baseProp.readlines():
        if cmp(line.strip(), "application.testcase-file=") != 0:
            newProp.write(line)
        else:
            newProp.write("application.testcase-file=" + casename.strip())
    
    # os.system("cp rundir/base.properties " + rundir/properties/)
    newProp.close()
    baseProp.close()


    # run replayer
    os.system("ant -v -Dproperties=" + propName + " -f jfcreplayer.xml")

    # get .ser file
    serName = casename.strip() + ".ser"
    os.system("cp cobertura.ser rundir/sers/" + serName)


    print "*****************************", counter

    # merge
    os.chdir("rundir")
    os.system("./cobertura-merge.sh --datafile sers/" + serName + ".f cobertura_original.ser " +
              " sers/" + serName)



    # generate report

    os.system("./cobertura-report.sh --format html --datafile sers/" + serName
              + ".f --destination reports/" + casename.strip() + " src/" )
    os.system("./cobertura-report.sh --format xml --datafile sers/" + serName
              + ".f --destination reports/" + casename.strip() + " src/" )

    
    os.chdir("..")
    
    
baseProp.close()
