#!/usr/bin/python
################################################################################
#
# File: parse.py
# Author: Teng Long(tlongcn@gmail.com)
# Usage: python parse.py model.in text.in number_of_sentences_to_process result_out.txt timing_out.txt
# Description:
#   Read the PCFG model from model.in, and parse the POS tag sequences
#   in text.in line by line. Output to stdout.
#
################################################################################


import sys
import timeit
import threading

class Node:
    head = ''
    left = ''
    right = ''

def backtrace_rec(start, end, tag, zeta, terminals): # trace (0, 4, NP), as e.g.
    if (start, end, tag) not in zeta:
        return "Error in backtracing!"
    
    
    track = zeta[(start, end, tag)]
    tagString = idSymDict[tag]
    if '~' not in tagString:
        result = '( ' + tagString + ' '
    else:
        # result = '( ' + tag + ' '
        result = ''

    # left child
    if track[1] in terminals:
    # if '~' not in idSymDict[track[1]]:
        result += '( '
        result += idSymDict[track[1]]
        result += ' '
        result += 'W' + idSymDict[track[1]].lower() + ' ) '
    else:
        result += backtrace_rec(start, track[0], track[1], zeta, terminals)
        result += ' '

    # right child
    if track[2] in terminals:
    # if '~' not in idSymDict[track[2]]:
        result += '( '
        result += idSymDict[track[2]]
        result += ' '
        result += 'W' + idSymDict[track[2]].lower() + ' ) '
    else:
        result += backtrace_rec(track[0], end, track[2], zeta, terminals)
        result += ' '

    if '~' not in tagString:
        result += ')'
    # else:
        # result += ')'
    
    return result.strip()
    

# CYK backtracing, return the result in a tree
def backtrace(S, zeta, n, terminals):

    if S in terminals:
        result = '( TOP (' + S + ' ' + 'W' + S.lower() + ' ) )'
        return result
    else:
        result = backtrace_rec(0, n, S, zeta, terminals)
        result = '( TOP ' + result + ' )'
        if "Error in backtracing!" not in result:
            return result
        else:
            return "Error, Cannot parse this sentence."


# CYK parsing
def cyk(in_string, model, S, symIdDict, idSymDict):
    treeRules = model[0]
    topRules = model[1]

    # print "parsing", in_string.strip()
    tags = in_string.split()

    terminals = set(tags)
    
    pi = {}                             # pi[(i, j, tags[i-j])] = probability
    zeta = {}                           # backtrack
    n = len(tags)                       # number of tags

    # optimized pi
    pi2 = {}
    for i in range(0, n+1):
        pi2[i] = {}
        for j in range(i+1, n+1):
            pi2[i][j] = {}
    
    


    for i in range(1, n+1):             
        key = (i-1, i, tags[i-1])
        pi[key] = 1.0
        pi2[i-1][i][symIdDict[tags[i-1]]] = 1.0




    begin = timeit.default_timer()
    for s in range(2, n+1):             # for s = 2 to n
        for b in range(0, n-s+1):       # for b = 0 to n-s
            for m in range(b+1, b+s):   # for m = b+1 to b+s-1


                for B in treeRules:
                    if B not in pi2[b][m]:
                        continue

                    for C in treeRules[B]:
                        if C not in pi2[m][b+s]:
                            continue

                        for A in treeRules[B][C]:
                    
                            probability = pi2[b][m][B] * pi2[m][b+s][C] * treeRules[B][C][A]
                            if A not in pi2[b][b+s] or \
                                   pi2[b][b+s][A] < probability:
                                pi2[b][b+s][A] = probability
                                zeta[(b, b+s, A)] = (m, B, C)
                            

                    
    # print "loops:", (timeit.default_timer() - begin)                    
    
    begin = timeit.default_timer()
    # find initial rule
    S = None
    max_prob = 0
    for rule in topRules:
        # print idSymDict[rule[0]], '->', idSymDict[rule[1]]
        A = rule[1]


        if A not in pi2[0][n]:
            continue


        # print "here here tada...."
        prob = pi2[0][n][A] * topRules[rule]
        

        if prob > max_prob:
            S = A
            max_prob = prob

    if S == None:
        print "wired, S not found."
        exit()
    
    terminals2 = set()
    for item in terminals:
        terminals2.add(symIdDict[item])
    
    result = backtrace(S, zeta, n, terminals2)

    # print "back tracing:", (timeit.default_timer() - begin)                        

    return result




    
if __name__ == "__main__":

    if len(sys.argv) != 6:

        print "Usage: python parse.py model.in text.in number_of_sentences_to_process result_out.txt timing_out.txt"
        exit()

    fdmodel = open(sys.argv[1])
    fdtext = open(sys.argv[2])
    num_to_process = int(sys.argv[3])
    fdout = open(sys.argv[4], 'w')
    fdtime = open(sys.argv[5], 'w')
    rules = {}                              # rules with probabilities

    # read rules
    for line in fdmodel.readlines():
        line = line.strip()
        if line.startswith('#'):    # ignore comments
            continue
        rule, probability = line.split('=')
        rules[rule.strip()] = float(probability.strip())


    # symbol sets, and use int for symbols in rules
    S = set()                           # all symbols
    V = set()                           # non-terminals
    T = set()                           # terminals

    for rule in rules:
        terms = rule.split()
        if len(terms) == 4:
            A = terms[0]
            B = terms[2]
            C = terms[3]
            S.add(A)
            S.add(B)
            S.add(C)
            V.add(A)
        else:
            A = terms[0]
            B = terms[2]
            S.add(A)
            S.add(B)
            V.add(A)
    for item in S:
        if item not in V:
            T.add(item)



    symIdDict = {}                      # symbol to ID
    idSymDict = {}                      # ID to symbol
    symCnt = 0

    for item in S:
        symIdDict[item] = symCnt
        idSymDict[symCnt] = item
        symCnt += 1

    newRules = {}                        # (A B C p) or (A B p)    
    for rule in rules:
        terms = rule.split()
        if len(terms) ==4:
            A = terms[0]
            B = terms[2]
            C = terms[3]
            newRules[(symIdDict[A], symIdDict[B], symIdDict[C])] = rules[rule]
        else:
            A = terms[0]
            B = terms[2]
            newRules[(symIdDict[A], symIdDict[B])] = rules[rule]   

    # classify rules by A->B and A->B C, and re-organize A->B C rules
    treeRules = {}
    topRules = {}


    for rule in newRules:
        if len(rule) == 2:
            topRules[rule] = newRules[rule]
            continue

        # A -> B C
        A, B, C = rule
        if B not in treeRules:
            treeRules[B] = {}
        if C not in treeRules[B]:
            treeRules[B][C] = {}
        treeRules[B][C][A] = newRules[rule]


    rulePack = [treeRules, topRules]

    lineCnt = 1
    

    lines = fdtext.readlines()
    print "total lines:", len(lines)
    print "total lines to process:", num_to_process
    

    if num_to_process > len(lines):
        num_to_process = len(lines)

    lineCnt = 0
    total_time = 0
    for line in lines:
        if lineCnt == num_to_process:
            break
        lineCnt += 1

        begin = timeit.default_timer()
        result = cyk(line, rulePack, S, symIdDict, idSymDict)
        end = timeit.default_timer()
        print >> fdout, result
        print >> fdtime, "line", lineCnt, "takes", (end - begin), "seconds."
        print "line", lineCnt, "takes", (end - begin), "seconds."
        total_time += (end - begin)

    print >> fdtime, "Processing", num_to_process, "sentences take", total_time, "seconds."
    print >> fdtime, "Avg time per sentence:", 1.0 * total_time / num_to_process

    fdmodel.close()
    fdtext.close()
    fdout.close()
    fdtime.close()

    exit()
