import os
import sys

# clear all existing instrumentations.
cmd = "rm -rf cobertura.ser"
os.system(cmd)

# Check whether the 
if not os.path.exists("JabRef-2.6/"):
    print "Error: 'JabRef-2.6' directory not exists."
    sys.exit(1)
else:
    print "Good by now."

# creating the instrumented directory
cmd = "cp -r JabRef-2.6 JabRef-2.6-inst"
os.system(cmd)

# begin to instrument
cmd = "./cobertura-instrument.sh JabRef-2.6-inst/com/jgoodies/uif_lite/"
os.system(cmd)

cmd = "./cobertura-instrument.sh JabRef-2.6-inst/gnu/"
os.system(cmd)

cmd = "./cobertura-instrument.sh JabRef-2.6-inst/wsi/"
os.system(cmd)

cmd = "./cobertura-instrument.sh JabRef-2.6-inst/net/sf/"
os.system(cmd)
