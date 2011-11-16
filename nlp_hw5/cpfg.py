#!/usr/bin/python
################################################################################
#
# File: pcfg.py
# Author: Teng Long(tlongcn@gmail.com)
# Usage: python cpfg.py train.in model.out
# Description:
#   Build the probabilistic cotext-free grammer model on
#     trainning set, and save it in a file.
#   The PCFG is left-factorized already.
#
################################################################################


import sys


# wanna use the sexpr_tokenize(my_str) function
from nltk.tokenize import *

# a parth tree Node
class Node:
    head = None
    childList  = None

# a parth tree
class Tree:
    root = None

    rule_buffer = None

    def parseRec(self, in_string):
        in_string = in_string.strip()
        if (not in_string.startswith('(')) or (not in_string.endswith(')')):
            print >> sys.stderr, "Error when constructing a parse tree."
            print >> sys.stderr, "string:", in_string
            sys.exit(1)



        afterPeal = in_string[1:-1].strip()
        if '(' not in afterPeal:        # already get to a leaf node
            pair = afterPeal.split()
            if len(pair) != 2:
                print >> sys.stderr, "Wired, leaf has more than 2 elements."
                sys.exit(1)
            tmpNode = Node()
            tmpNode.head = pair[0]
            tmpNode.childList = pair[1]
            return tmpNode
        else:
            elements = sexpr_tokenize(afterPeal)
            tmpNode = Node()
            tmpNode.head = elements[0]
            tmpNode.childList = []
            for item in elements[1:]:
                tmpNode.childList.append(self.parseRec(item))
            return tmpNode
        
    def __init__(self, in_string):
        self.root = self.parseRec(in_string)


    def printNode(self, node):
        if type(node.childList) != type("string"):
            for item in node.childList:
                print node.head , '--' , item.head
                self.printNode(item)
            print ''
        else:
            print node.head, '--', node.childList
            print ''

    def printTree(self):
        self.printNode(self.root)


    def getRuleNode(self, node, buffer):
        if type(node.childList) == type("str"):
            return                      # skip the leaves.
            # rule = node.childList
        else:
            rule = ''
            for item in node.childList:
                rule = rule + item.head
                rule = rule + ' '
            rule.strip()
            rule = node.head + ' -> ' + rule
        if rule not in buffer:
            buffer[rule] = 1
        else:
            buffer[rule] += 1 

        if type(node.childList) != type("str"):
            for item in node.childList:
                self.getRuleNode(item, buffer)
        

    def getRules(self):
        self.rule_buffer = {}
        self.getRuleNode(self.root, self.rule_buffer)
        return self.rule_buffer
        

def leftFactorize(rule):  # A -> B C | D | E F
    left = rule.split('->')[0].strip()
    rightList = rule.split('->')[1].split('|')
    # print "left:", left
    # print "rightList:", rightList

    result = []
    
    for item in rightList:
        tagList = item.split()
        # print tagList

        rightCount = len(tagList)
        if rightCount ==1 or rightCount == 2:
            result.append(left + ' -> ' + item.strip())
        else:
            tmpLeft = left
            tmpRight = None
            while rightCount > 2:
                tmpRight = tmpLeft + '~' + tagList[0]
                result.append(tmpLeft + ' -> ' + tagList[0] + ' ' + tmpRight)
                del tagList[0]
                tmpLeft = tmpRight
                rightCount -= 1
            result.append(tmpLeft + ' -> ' + ' '.join(tagList))
    return result


########################################
#
# Main part
#
########################################

# Input text file as trainning set; output text as model
if len(sys.argv) != 3:
    print "Usage: python q2.py input_file.txt output_file.mod"
    exit()

fd = open(sys.argv[1])

outfd = open(sys.argv[2], 'w')

totalRules = {}           # rules before left-factorization, with freq

for line in fd.readlines():
    line = line.strip()
    if len(line) == 0:
        continue
    tree = Tree(line)

    rules = tree.getRules()
    for item in rules:
        if item not in totalRules:
            totalRules[item] = rules[item]
        else:
            totalRules[item] += rules[item]

factorizedRules = {}       # rules after left-factorization, with freq
for item in totalRules:
    result = leftFactorize(item)
    for ii in result:
        if ii not in factorizedRules:
            factorizedRules[ii] = totalRules[item]
        else:
            factorizedRules[ii] += totalRules[item]

print "number of rules:", len(factorizedRules)
print "This count includes 'Top -> **' ones." 
print ''


probRulesDict = {}                      # rules with their probability
leftDict = {}                           # freq of left rules

# first scan, populate leftDict;
for item in factorizedRules:
    left = item.split('->')[0].strip()
    if left not in leftDict:
        leftDict[left] = factorizedRules[item]
    else:
        leftDict[left] += factorizedRules[item]

# second scan, populate probRulesDict;
for item in factorizedRules:
    left = item.split('->')[0].strip()
    print >> outfd, item, '=', 1.0 * factorizedRules[item] / leftDict[left]


