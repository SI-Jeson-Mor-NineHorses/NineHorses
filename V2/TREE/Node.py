import random
from V2.MCTS.State import State
from V2.MCTS.UCT import calcUctValue


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
            self.state = State(state=node.getState())
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
        best.getState().score = calcUctValue(self.getState().getVisitCount(), best.getState().getWinScore(), best.getState().getVisitCount())
        for child in self.childArray:
            child.getState().score = calcUctValue(self.getState().getVisitCount(), child.getState().getWinScore(), child.getState().getVisitCount())
            # print(child.getState().score)
            if child.getState().score > best.getState().score:
                best = child
        # print(best.getState().score, end="")
        return best
