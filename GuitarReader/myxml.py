##################################################
#
# Filename: myxml.py
# Description:
#   providing xml parsing, sorting and comparison.
#
##################################################

import sys

from lxml import etree
from lxml import objectify


class Xnode:
    tag = None
    text = None
    children = None


# 1: root1 > root2; 0: root1 == root2; -1: root1 < root2
def comp(root1, root2): # recursively compare subtrees.
    if root1.tag > root2.tag:
        return 1
    elif root1.tag < root2.tag:
        return -1
    else:
        if root1.text > root2.text:
            return 1
        elif root1.text < root2.text:
            return -1
        else:
            kids1 = root1.children
            kids2 = root2.children
            if kids1 == None and kids2 == None:
                return 0
            if kids2 == None:
                return 1
            elif kids1 == None:
                return -1
            elif len(kids1) > len(kids2):
                return 1
            elif len(kids1) < len(kids2):
                return -1
            else:
                for i in range(0, len(kids1)):
                    result = comp(kids1[i], kids2[i])
                    if result != 0:
                        return result
                return 0
                    
                


def printXnode(xnode, level=''):
    print level, "tag:", xnode.tag, "\t", "text:", xnode.text
    level += '\t'

    if xnode.children != None:
        for item in xnode.children:
            printXnode(item, level)

def printXML(xnode, level=''):
    if xnode.children == None:
        if xnode.text != None:
            print level, '<' + xnode.tag + '>' + xnode.text + '</' + xnode.tag + '>'
        else:
            print level, '<' + xnode.tag + '>' + '</' + xnode.tag + '>'
    else:
        if xnode.text == None:
            print level, '<' + xnode.tag + '>'
        else:
            print level, '<' + xnode.tag + '>' + str(xnode.text).strip()
        for item in xnode.children:
            printXML(item, level +'    ')
        print level, '</' + xnode.tag + '>'


class Xtree:
    root = None


    def __recParse(self, objElem):
        node = Xnode()
        node.tag = objElem.tag
        node.text = objElem.text

        l = [el for el in objElem.iterchildren()]

        # if len(l) != 0:

        children = []
        for el in l:
            children.append(self.__recParse(el))
        if len(children) != 0:
            node.children = children
        return node

    def parseFile(self, fd):
        etree1 = objectify.parse(fd)
        self.root = self.__recParse(etree1.getroot())



    def __ordered(self, xnode):
        if xnode.children == None:
            None
        else:
            for item in xnode.children:
                self.__ordered(item)
            xnode.children = sorted(xnode.children, cmp = comp)

    def formalize(self):
        self.__ordered(self.root)

        
    
    
if __name__ == "__main__":
    xmlfile1 = open(sys.argv[1])
    xmlfile2 = open(sys.argv[2])
    
    xtree1 = Xtree()
    xtree1.parseFile(xmlfile1)
    
    xtree2 = Xtree()
    xtree2.parseFile(xmlfile2)

    # print comp(xtree1.root, xtree2.root)

    # printXnode(xtree1.root)

    xtree1.formalize()

    # printXnode(xtree1.root)
    printXML(xtree1.root)
