import random
from MCTS.State import State


class Node:
    def __init__(self, node=None, state=None, parent=None, childArray=None):
        if node is None:
            if state is None:
                self.state = State()
            else:
                self.state = state
            if childArray is None:
                self.childArray = []
            else:
                self.childArray = childArray
            if parent is None:
                self.parent = None
            else:
                self.parent = parent
        else:
            self.childArray = []
            self.state = State(node.getState())
            if node.getParent() is not None:
                self.parent = node.getParent()
            childArray = node.getChildArray()
            for child in childArray:
                self.childArray.append(Node(child))

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getChildArray(self):
        return self.childArray

    def setChildArray(self, childArray):
        self.childArray = childArray

    def getRandomChildNode(self):
        # noOfPossibleMoves = len(self.childArray)
        # selectRandom = random.choice(self.childArray)
        # return self.childArray[selectRandom]
        return random.choice(self.childArray)

    def getChildWithMaxScore(self):
        best = self.childArray[0]
        for child in self.childArray:
            if child.getState().getVisitCount() > best.getState().getVisitCount():
                best = child
        return best
