#!/usr/bin/python

import sys

infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')

lines = infile.readlines()

for line in lines:
    if line.startswith('SF:'):
        # print line
        segs = line.split('/')
        # print segs
        for i in range(0, len(segs) - 4):
            if segs[i] == segs[i+2] and segs[i+1] == segs[i+3]:
                a = segs[i]
                b = segs[i+1]
                segs.remove(a)
                segs.remove(b)
                continue
        for i in range(0, len(segs) - 6):
            if segs[i] == segs[i+3] and segs[i+1] == segs[i+4] and segs[i+2] == segs[i+5]:
                a = segs[i]
                b = segs[i+1]
                c = segs[i+2]
                segs.remove(a)
                segs.remove(b)
                segs.remove(c)
                continue
            
        for i in range(0, len(segs) - 2):
            if segs[i] == segs[i+1]:
                a = segs[i]
                segs.remove(a)
                break

            
        outfile.write('/'.join(segs))
    else:
        outfile.write(line)


infile.close()
outfile.close()

