#!/usr/bin/python

import os


##############################
#
# JAVA 15
#
##############################

# environment variables

os.environ['JAVA_HOME'] = "/home/tlong/Documents/work_737_paper/do_it_local/packages/jdk1.6.0_15"
os.environ['ANT_HOME'] = "/home/tlong/Documents/work_737_paper/do_it_local/packages/apache-ant-1.8.2"
env = os.getenv("JAVA_HOME") + '/bin:' + os.getenv("ANT_HOME") + '/bin:' + os.getenv("PATH")
os.environ["PATH"] = env
env = os.getenv("JAVA_HOME") + '/lib'
os.environ['CLASSPATH'] = env


cmd = "java -version"
os.system(cmd)

# copy rundir
cmd = "cp -r rundir_bk/ rundir"
os.system(cmd)


# run test
cmd = "rm -rf Project_log"
os.system(cmd)


cmd = "./run.py proj.list"
os.system(cmd)



# copy rundir
cmd = "cp -r Project_log rundir/"
os.system(cmd)

cmd = "rm -rf rundir15"
os.system(cmd)

cmd = "mv rundir rundir15"
os.system(cmd)



##############################
#
# JAVA 16
#
##############################

# environment variables

os.environ['JAVA_HOME'] = "/home/tlong/Documents/work_737_paper/do_it_local/packages/jdk1.6.0_16"
os.environ['ANT_HOME'] = "/home/tlong/Documents/work_737_paper/do_it_local/packages/apache-ant-1.8.2"
env = os.getenv("JAVA_HOME") + '/bin:' + os.getenv("ANT_HOME") + '/bin:' + os.getenv("PATH")
os.environ["PATH"] = env
env = os.getenv("JAVA_HOME") + '/lib'
os.environ['CLASSPATH'] = env


cmd = "java -version"
os.system(cmd)

# copy rundir
cmd = "cp -r rundir_bk/ rundir"
os.system(cmd)


# run test
cmd = "rm -rf Project_log"
os.system(cmd)


cmd = "./run.py proj.list"
os.system(cmd)

# copy rundir
cmd = "cp -r Project_log rundir/"
os.system(cmd)

cmd = "rm -rf rundir16"
os.system(cmd)

cmd = "mv rundir rundir16"
os.system(cmd)

##############################
#
# JAVA 21
#
##############################

# environment variables

os.environ['JAVA_HOME'] = "/home/tlong/Documents/work_737_paper/do_it_local/packages/jdk1.6.0_21"
os.environ['ANT_HOME'] = "/home/tlong/Documents/work_737_paper/do_it_local/packages/apache-ant-1.8.2"
env = os.getenv("JAVA_HOME") + '/bin:' + os.getenv("ANT_HOME") + '/bin:' + os.getenv("PATH")
os.environ["PATH"] = env
env = os.getenv("JAVA_HOME") + '/lib'
os.environ['CLASSPATH'] = env


cmd = "java -version"
os.system(cmd)

# copy rundir
cmd = "cp -r rundir_bk/ rundir"
os.system(cmd)


# run test
cmd = "rm -rf Project_log"
os.system(cmd)


cmd = "./run.py proj.list"
os.system(cmd)

# copy rundir
cmd = "cp -r Project_log rundir/"
os.system(cmd)

cmd = "rm -rf rundir21"
os.system(cmd)

cmd = "mv rundir rundir21"
os.system(cmd)

##############################
#
# JAVA 24
#
##############################

# environment variables

os.environ['JAVA_HOME'] = "/home/tlong/Documents/work_737_paper/do_it_local/packages/jdk1.6.0_24"
os.environ['ANT_HOME'] = "/home/tlong/Documents/work_737_paper/do_it_local/packages/apache-ant-1.8.2"
env = os.getenv("JAVA_HOME") + '/bin:' + os.getenv("ANT_HOME") + '/bin:' + os.getenv("PATH")
os.environ["PATH"] = env
env = os.getenv("JAVA_HOME") + '/lib'
os.environ['CLASSPATH'] = env


cmd = "java -version"
os.system(cmd)

# copy rundir
cmd = "cp -r rundir_bk/ rundir"
os.system(cmd)


# run test
cmd = "rm -rf Project_log"
os.system(cmd)


cmd = "./run.py proj.list"
os.system(cmd)

# copy rundir
cmd = "cp -r Project_log rundir/"
os.system(cmd)

cmd = "rm -rf rundir24"
os.system(cmd)

cmd = "mv rundir rundir24"
os.system(cmd)
