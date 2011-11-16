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
    if '~' not in tag:
        result = '( ' + tag + ' '
    else:
        # result = '( ' + tag + ' '
        result = ''

    # left child
    if track[1] in terminals:
        result += '( '
        result += track[1]
        result += ' '
        result += 'W' + track[1].lower() + ' ) '
    else:
        result += backtrace_rec(start, track[0], track[1], zeta, terminals)
        result += ' '

    # right child
    if track[2] in terminals:
        result += '( '
        result += track[2]
        result += ' '
        result += 'W' + track[2].lower() + ' ) '
    else:
        result += backtrace_rec(track[0], end, track[2], zeta, terminals)
        result += ' '

    if '~' not in tag:
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

# with full initialization of pi
def cyk2(in_string, model):
    tags = in_string.split()
    n = len(tags)
    V = set()
    for rule in model:
        left = rule.split('->')[0].strip()
        V.add(left)

    pi = {}
    zeta = {}

    for i in range(0, n+1):
        for j in range(0, n+1):
            for item in V:
                pi[(i, j, item)] = 0.0


    for i in range(1, n+1):
        pi[(i-1, i, tags[i-1])] = 1.0

    for s in range(2, n+1):
        for b in range(0, n-s+1):
            for m in range(b+1, b+s):
                for rule in model:
                    left, right = rule.split('->')
                    A = left.strip()
                    rights = right.split()
                    if len(rights) == 1:
                        continue
                    B = rights[0]
                    C = rights[1]

                    if (b, m, B) not in pi:
                        continue
                    if (m, b+s, C) not in pi:
                        continue

                    probability = pi[(b, m, B)] * pi[(m, b+s, C)] * model[rule]

                    if ((b, b+s, A) not in pi) or probability > pi[(b, b+s, A)]:
                        pi[(b, b+s, A)] = probability
                        zeta[(b, b+s, A)] = (m, B, C)
                    


    # find max S
    A = None
    max_prob = 0.0
    for rule in model:
        left = rule.split('->')[0].strip()
        if left != "TOP":
            continue
        right = rule.split('->')[1].strip()

        if (0, n, right) not in pi:
            continue
        prob = pi[(0, n, right)] * model[rule]
        if prob > max_prob:

            A = right
            max_prob = prob


    result = backtrace(A, zeta, n, tags)
    return result;


# CYK parsing
def cyk(in_string, model):
    # print "parsing", in_string.strip()
    tags = in_string.split()

    terminals = set(tags)
    
    pi = {}                             # pi[(i, j, tags[i-j])] = probability
    zeta = {}                           # backtrack
    n = len(tags)                       # number of tags



    # filter out irrelavent rules
    begin = timeit.default_timer()

    model_se = {}
    for item in model:
        left, rights = item.split('->')
        left = left.strip()

        rights = rights.split()
        if len(rights) == 1:
            continue
        else:
            model_se[(left, rights[0], rights[1])] = model[item]


    print "filter:", (timeit.default_timer() - begin)


    for i in range(1, n+1):             # for i=1 to n, pi[i-1, i, tao(i)] <- 1
        key = (i-1, i, tags[i-1])
        pi[key] = 1
        # print "pi[", key, ']:', pi[key]



    begin = timeit.default_timer()
    for s in range(2, n+1):             # for s = 2 to n
        for b in range(0, n-s+1):       # for b = 0 to n-s
            for m in range(b+1, b+s):   # for m = b+1 to b+s-1
                for rule in model_se:      # for all A,B,C that A -> B C
                    A, B, C = rule

                    if (b, m, B) not in pi:
                        continue
                    if (m, b+s, C) not in pi:
                        continue
                    probability = pi[(b, m, B)] * pi[(m, b+s, C)] * model_se[rule]
                    
                    # update pi
                    if ((b, b+s, A) not in pi) or \
                           (probability > pi[(b, b+s, A)]):
                        pi[(b, b+s, A)] = probability
                        zeta[(b, b+s, A)] = (m, B, C) # backtracks

                    
    print "loops:", (timeit.default_timer() - begin)                    
    
    begin = timeit.default_timer()
    # find initial rule
    S = None
    max_prob = 0
    for rule in model:
        if not rule.startswith('TOP'):
            continue
        A = rule.split('->')[1].strip()
        if (0, n, A) not in pi:
            continue
        prob = pi[(0, n, A)] * model[rule]
        if prob > max_prob:
            S = A
            max_prob = prob


    result = backtrace(S, zeta, n, terminals)
    # print "time for backtracing:", (timeit.default_timer() - time2)
    print "back tracing:", (timeit.default_timer() - begin)                        

    return result




    # print 'S:', Sp
    
    # for item in pi:
    #     print 'pi[', item, ']:', pi[item]

    # print ''
    # for item in zeta:
    #     print 'zeta[', item, ']:', zeta[item]


class Cyk_thread(threading.Thread):
    def __init__(self, sentences, rules, resultSet):
        threading.Thread.__init__(self)
        self.sentences = sentences
        self.rules = rules
        self.resultSet = resultSet

    def run(self):
        for item in self.sentences:
            line = item[1]
            start = timeit.default_timer()
            print "\nprocessing sentence", item[0]
            result = cyk(line, self.rules)
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
            
        threads.append(Cyk_thread(sentences, rules, tmpResult))
        
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
    
