#################################################
#
# Filename: myxml.py
# Description:
#   providing xml parsing, sorting and comparison.
# Update:
#   6/19/11: parent for each node added.
#
##################################################

import sys
import codecs

from lxml import etree
from lxml import objectify


class Xnode:
    tag = None
    text = None
    children = None
    parent = None

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
                    

def path(node):
    if node.parent != None:
        # find ids for current path from the parent's children list
        eId = ''
        for item in node.parent.children:
            if 'EventId' == item.tag:
                eId = "-EventId:" + item.text
                break
        wId = ''
        if node.tag == 'Property':
            for item in node.parent.children:
                if item.children[0].text == 'ID':
                    wId = '-widgetId:' + item.children[1].text
                    break
        if node.text == None:
            return path(node.parent) + "<" + node.tag + eId + wId + ">"
        else:
            return path(node.parent) + "<" + node.tag + ',' + str(node.text) + eId + wId + ">"
    else:
        if node.text == None:
            return '<' + node.tag + '>'
        else:
            return '<' + node.tag + ',' + str(node.text) + '>'


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



def writeXML(xnode, fd, level=''):
    if xnode.children == None:
        if xnode.text != None:
            # print level, '<' + xnode.tag + '>' + xnode.text + '</' + xnode.tag + '>'
            string = level + '<' + xnode.tag + '>' + xnode.text + '</' + xnode.tag + '>\n'
            fd.write(string)
        else:
            # print level, '<' + xnode.tag + '>' + '</' + xnode.tag + '>'
            string = level + '<' + xnode.tag + '>' + '</' + xnode.tag + '>\n'
            fd.write(string)
    else:
        if xnode.text == None:
            # print level, '<' + xnode.tag + '>'
            string = level + '<' + xnode.tag + '>\n'
            fd.write(string)
        else:
            # print level, '<' + xnode.tag + '>' + str(xnode.text).strip()
            string = level + '<' + xnode.tag + '>' + str(xnode.text).strip() + '\n'
            fd.write(string)
        for item in xnode.children:
            # printXML(item, level +'    ')
            writeXML(item, fd, level + '    ')
        # print level, '</' + xnode.tag + '>'
        string = level + '</' + xnode.tag + '>\n'
        fd.write(string)

class Xtree:
    root = None


    def __recParse(self, objElem, parent=None):
        node = Xnode()
        node.tag = objElem.tag
        if objElem.text == None or len(objElem.text) < 50:
            node.text = objElem.text
        else:
            node.text = 'Default Input String For Guitar'
        node.parent = parent
        
        l = [el for el in objElem.iterchildren()]

        # if len(l) != 0:

        children = []
        for el in l:
            children.append(self.__recParse(el, node))
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

        



def diffTree(treeRoot1, treeRoot2):
    if treeRoot1.tag != treeRoot2.tag or treeRoot1.text != treeRoot2.text:
        print "path_1:", path(treeRoot1), "text:", treeRoot1.text
        print "path_2:", path(treeRoot2), "text:", treeRoot2.text, '\n'
        return
    elif treeRoot1.children == None and treeRoot2.children == None:
        return
    elif treeRoot1.children == None or treeRoot2.children == None:
        print path(treeRoot1), ': children:', treeRoot1.children
        print path(treeRoot2), ': children:', treeRoot2.children, '\n'
        return
    elif len(treeRoot1.children) != len(treeRoot2.children):
        print path(treeRoot1), ': # children:', len(treeRoot1.children)
        print path(treeRoot2), ': # children:', len(treeRoot2.children), '\n'
        return
    else:
        for i in range(0, len(treeRoot1.children)):
            diffTree(treeRoot1.children[i], treeRoot2.children[i])
        
    
    
if __name__ == "__main__":
    xmlfile1 = codecs.open(sys.argv[1], encoding='utf-8', mode='r')
    xmlfile2 = codecs.open(sys.argv[2], encoding='utf-8', mode='w')
    
    xtree1 = Xtree()
    xtree1.parseFile(xmlfile1)
    
    # xtree2 = Xtree()
    # xtree2.parseFile(xmlfile2)

    # print comp(xtree1.root, xtree2.root)

    # printXnode(xtree1.root)

    xtree1.formalize()

    # printXnode(xtree1.root)
    # printXML(xtree1.root)

    # print path(xtree1.root.children[0].children[0])
    writeXML(xtree1.root, xmlfile2)
    xmlfile1.close()
    xmlfile2.close()
