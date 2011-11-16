#!/usr/bin/python
################################################################################
#
# File: parse.py
# Author: Teng Long(tlongcn@gmail.com)
# Usage: python parse.py model.in text.in number_of_sentences_to_process number_of_threads out.txt
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
        result += '( '
        result += idSymDict[track[1]]
        result += ' '
        result += 'W' + idSymDict[track[1]].lower() + ' ) '
    else:
        result += backtrace_rec(start, track[0], track[1], zeta, terminals)
        result += ' '

    # right child
    if track[2] in terminals:
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
    
    


    # filter out irrelavent rules
    begin = timeit.default_timer()

    model_se = {}
    for item in model:
        if len(item) == 2:
            continue
        else:
            model_se[item] = model[item]


    # print "filter:", (timeit.default_timer() - begin)


    for i in range(1, n+1):             # for i=1 to n, pi[i-1, i, tao(i)] <- 1
        key = (i-1, i, tags[i-1])
        pi[key] = 1.0
        pi2[i-1][i][symIdDict[tags[i-1]]] = 1.0
        # print "pi[", key, ']:', pi[key]



    begin = timeit.default_timer()
    for s in range(2, n+1):             # for s = 2 to n
        for b in range(0, n-s+1):       # for b = 0 to n-s
            for m in range(b+1, b+s):   # for m = b+1 to b+s-1
                for rule in model_se:      # for all A,B,C that A -> B C
                    A, B, C = rule


                    # if (b, m, B) not in pi:
                    #     continue

                    if B not in pi2[b][m]:
                        continue
                    
                    # if (m, b+s, C) not in pi:
                    #     continue

                    if C not in pi2[m][b+s]:
                        continue

                    # probability = pi[(b, m, B)] * pi[(m, b+s, C)] * model_se[rule]
                    probability = pi2[b][m][B] * pi2[m][b+s][C] * model_se[rule]
                    
                    # update pi

                    # if ((b, b+s, A) not in pi) or \
                    #        (probability > pi[(b, b+s, A)]):
                    #     pi[(b, b+s, A)] = probability
                    #     zeta[(b, b+s, A)] = (m, B, C) # backtracks

                    if A not in pi2[b][b+s] or \
                       pi2[b][b+s][A] < probability:
                        pi2[b][b+s][A] = probability
                        zeta[(b, b+s, A)] = (m, B, C)

                    
    print "loops:", (timeit.default_timer() - begin)                    
    # for ii in pi2:
    #     for jj in pi2[ii]:
    #         for kk in pi2[ii][jj]:
    #             print (ii, jj, kk), '=', pi2[ii][jj][kk]
    
    begin = timeit.default_timer()
    # find initial rule
    S = None
    max_prob = 0
    for rule in model:
        if idSymDict[rule[0]] != "TOP":
            continue

        A = rule[1]

        # if (0, n, A) not in pi:
        #     continue
        # prob = pi[(0, n, A)] * model[rule]

        if A not in pi2[0][n]:
            continue

        prob = pi2[0][n][A] * model[rule]
        

        if prob > max_prob:
            S = A
            max_prob = prob

    terminals2 = set()
    for item in terminals:
        terminals2.add(symIdDict[item])
    
    result = backtrace(S, zeta, n, terminals2)

    # print "back tracing:", (timeit.default_timer() - begin)                        

    return result




class Cyk_thread(threading.Thread):
    def __init__(self, sentences, rules, symSet, symIdDict, idSymDict, resultSet):
        threading.Thread.__init__(self)
        self.sentences = sentences
        self.rules = rules
        self.resultSet = resultSet
        self.symSet = symSet

    def run(self):
        for item in self.sentences:
            line = item[1]
            start = timeit.default_timer()
            print "\nprocessing sentence", item[0]
            result = cyk(line, self.rules, self.symSet, symIdDict, idSymDict)
            duration = timeit.default_timer() - start
            
            self.resultSet.append((item[0], result, duration))
    
if __name__ == "__main__":

    if len(sys.argv) != 6:
        print "Usage: python parse.py model.in text.in number_of_sentences_to_process number_of_threads out.txt"
        exit()

    fdmodel = open(sys.argv[1])
    fdtext = open(sys.argv[2])
    num_to_process = int(sys.argv[3])
    num_threads = int(sys.argv[4])
    fdout = open(sys.argv[5], 'w')

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

    # print "\nSymbol table:"
    # for item in S:
    #     print item, ':', symIdDict[item]


    # read input strings
    lineCnt = 1
    

    lines = fdtext.readlines()
    print "total lines:", len(lines)
    print "total lines to process:", num_to_process
    print "number of threads:", num_threads
    

    if num_to_process > len(lines):
        num_to_process = len(lines)

    if (num_to_process % num_threads) == 0:
        avg = num_to_process / num_threads
    else:
        avg = num_to_process / num_threads + 1

    threads = []
    resultSet = []                      # for multi-threading purpose

    total = 0
        
    for i in range(0, num_threads):
        tmpResult = []

        
        begin = i * avg
        end = (i + 1) * avg - 1

        if end > (num_to_process - 1):
            end = num_to_process - 1

        sentences = []
        for j in range(begin, end + 1):
            sentences.append((j, lines[j]))
            total += 1
            
        threads.append(Cyk_thread(sentences, newRules, S, symIdDict, idSymDict, tmpResult))
        
        resultSet.append(tmpResult)



    time_start = timeit.default_timer()
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    time_end = timeit.default_timer()

    results = []
    for i in range(0, num_threads):
        for item in resultSet[i]:
            results.append(item)

    print "result size:", len(results)

    sorted(results)

    for item in results:
        print >> fdout, item[1]
        print "line", item[0], "takes", item[2], "seconds."
        # print item


    print "total time spent on", num_to_process, "lines:", (time_end - time_start)
    print "Average time for a sentence:", 1.0 * (time_end - time_start) / num_to_process
    
