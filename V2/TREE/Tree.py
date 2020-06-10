from V2.TREE.Node import Node


class Tree:
    def __init__(self, root=None):
        if root is None:
            self.root = Node()
        else:
            self.root = root

    def getRoot(self):
        return self.root

    def setRoot(self, root):
        self.root = root

    def addChild(self, parent, child):
        parent.getChildArray().append(child)


def printTree(node, file=None, _prefix="", _last=True):
    # print implementation from https://vallentin.dev/2016/11/29/pretty-print-tree
    if node.getState().visitCount != 0 and node.getState().winScore != 0:
        print(_prefix, "`- [" if _last else "|- [", node.getState().playerNo, '] ',
              node.getState().move_from, node.getState().move_to, " ",
              node.getState().winScore, '/', node.getState().visitCount, ' = ',
              node.getState().score,
              sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.getChildArray())
    for i, child in enumerate(node.getChildArray()):
        _last = i == (child_count - 1)
        printTree(child, file, _prefix, _last)


def print_children_tree(node, file=None, _prefix="", _last=True):
    if node.getState().visitCount != 0 and node.getState().winScore != 0:
        print(_prefix, "`- [" if _last else "|- [", node.getState().playerNo, '] ',
              node.getState().move_from, node.getState().move_to, " ",
              node.getState().winScore, '/', node.getState().visitCount,
              sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.getChildArray())
    for i, child in enumerate(node.getChildArray()):
        _last = i == (child_count - 1)
        print(_prefix, "`- [" if _last else "|- [", child.getState().playerNo, '] ',
              child.getState().move_from, child.getState().move_to, " ",
              child.getState().winScore, '/', child.getState().visitCount, ' = ',
              child.getState().score,
              sep="", file=file)
