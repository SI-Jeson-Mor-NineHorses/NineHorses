from TREE.Node import Node


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
        parent.getChildArray().add(child)
