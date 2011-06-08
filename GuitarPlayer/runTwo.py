import os
import time

t1 = time.ctime()


cmd = "cp -r rundir_bk rundir"
os.system(cmd)

runcmd = "python run.py l3list.txt"
os.system(runcmd)

cmd = "rm -rf rundir/sers"
os.system(cmd)

cmd = "mv rundir rundir_round1"
os.system(cmd)

cmd = "cp -r rundir_bk rundir"
os.system(cmd)

os.system(runcmd)

cmd = "rm -rf rundir/sers"
os.system(cmd)

cmd = "mv rundir rundir_round2"
os.system(cmd)

t2 = time.ctime()

print "start:", t1
print "end:", t2
