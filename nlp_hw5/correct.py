import math
import time

def backtrace(l,h,A):
    if l+1<h:
        if (l,h,A) not in Bt:
            rule = "Can't backtrace further, not in grammar"
        else:
            z = Bt[(l,h,A)]
            (m,B,C) = z
            if "~" not in A:
                rule = "("+ A + " " + backtrace(l,m,B) + backtrace(m,h,C) + ")"
            else:
                rule = backtrace(l,m,B) + backtrace(m,h,C)
    else:
        rule = "(" + A + " W" + A.lower() + ")"
    return rule
rule = 'model.txt'
n1 = 'corpus/f2-21.test.parse-POSonly'
output = 'output.txt'
test = open(n1, 'r')
r = open(rule, 'r')
op = open(output, 'w')
S = []
B = []
rules = {}
B_rules = {}
top_rules = {}
for line in r:
    a = line.split()
    if a[0] != "TOP":
        rule = (a[0],a[2],a[3])
        rules[rule] = float(a[5])
        B.append(a[2])
    else:
        rule = (a[0],a[2])
        top_rules[rule] = float(a[4])
        S.append(a[2])
r.close()

B = list(set(B))

for b in B:
    C_rules = {}
    for rule in rules:
        (x,y,z) = rule
        if y == b:
            C_rules.setdefault(z, []).append(x)
    B_rules[b]=C_rules
           
print "Preprocessing done, starting CYK and timer"
t0 = time.time()
number = 100

for line in test:
    Pi = {}
    Bt = {}
    mlist = []
    tag_seq = line.split(' ')
    tag_seq.pop()
    i = 0
    n = len(tag_seq)
    short_rules = []

    for tag in tag_seq:
        X = (i,i+1,tag)
        Pi[X] = 1.0
        i += 1

    for i in range(2,n+1):
        for j in range(0,n-i+1):
            for k in range(j+1,j+i):
                mlist.append([j,k,i+j])

    for pos in mlist:
        j = pos[0]                      # start
        k = pos[1]                      # middle
        e = pos[2]                      # end
        for B in B_rules:
            if (j,k,B) in Pi:
                dt = B_rules[B]
                for C in dt:
                    if (k,e,C) in Pi:
                        for A in dt[C]:
                            rule = (A,B,C)
                            X1 = (j,k,B)
                            X2 = (k,e,C)
                            X3 = (j,e,A)
                            if rule not in rules:
                                rules[rule] = 0.0
                                                                            
                            p = Pi[X1] * Pi[X2] * rules[rule]
                    
                            if X3 not in Pi:
                                Pi[X3] = 0.0
                   
                            if (p>Pi[X3]):
                                Pi[X3] = p
                                b = (k,B,C)
                                Bt[X3] = b

    mx = 0.0
    START = '#'
    for s in S:
        X = (0,n,s)
        rule = ('TOP',s)
        if X not in Pi:
            Pi[X] = 0.0
        m = Pi[X]*top_rules[rule]
        if m>mx:
            START = s
            mx = m
    #now we backtrack
    rule = "(TOP " + backtrace(0,n,START) + ")\n"
    print rule
    op.write(rule)
    if number > 1:
        number -= 1
    else:
        break
print "Time: ", time.time()-t0, "sec"
test.close()
op.close()
