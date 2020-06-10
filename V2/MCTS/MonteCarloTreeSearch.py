# TODO: MonteCarloTreeSearch class
from V2.TREE.Tree import Tree, print_children_tree
from V2.TREE.Node import Node
from V2.MCTS import UCT
import time
import copy
import sys


class MonteCarloTreeSearch:
    def __init__(self):
        self.level = 3
        self.WIN_SCORE = 1
        self.opponent = 0

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def getMillisForCurrentLevel(self):
        return 2 * (self.level - 1) + 1

    def findNextMove(self, board, playerNo):
        start = int(round(time.time() * 1000))
        end = start + 20 * 1000 #* self.getMillisForCurrentLevel()

        self.opponent = 3 - playerNo
        tree = Tree()
        rootNode = tree.getRoot()
        rootNode.getState().setBoard(copy.deepcopy(board))
        rootNode.getState().setPlayerNo(self.opponent)

        while int(round(time.time() * 1000)) < end:
            #Phase 1 - Selection
            promisingNode = self.selectPromisingNode(rootNode)

            #Phase 2 - Expansion
            if promisingNode.getState().getBoard().checkStatus() == -1:
                if promisingNode.getState().getVisitCount() > 70:
                    self.expandNode(promisingNode)

            #Phase 3 - Simulation
            nodeToExplore = promisingNode
            if len(promisingNode.getChildArray()) > 0:
                nodeToExplore = promisingNode.getRandomChildNode()

            playoutResult = self.simulateRandomPlayout(nodeToExplore)

            #Phase 4 - Update
            self.backPropagation(nodeToExplore, playoutResult)

        # print(nodeToExplore.getState().winScore)
        winnerNode = rootNode.getChildWithMaxScore()
        print_children_tree(rootNode)
        # printTree(rootNode)

        print("# BEST #  [", winnerNode.getState().playerNo, '] ',
              winnerNode.getState().move_from, winnerNode.getState().move_to, " ",
              winnerNode.getState().winScore,'/',winnerNode.getState().visitCount, ' = ',
              winnerNode.getState().score)
        tree.setRoot(winnerNode)
        return winnerNode.getState().getBoard()

    def selectPromisingNode(self, rootNode):
        # node = copy.deepcopy(rootNode)
        node = rootNode
        # print(node.getChildArray())
        while len(node.getChildArray()) != 0:
            node = UCT.findBestNodeWithUCT(node)
        return node

    def expandNode(self, node):
        possibleStates = node.getState().getAllPossibleStates()
        # print(possibleStates)
        for state in possibleStates:
            newNode = Node(state=state)
            newNode.setParent(node)
            newNode.getState().setPlayerNo(node.getState().getOpponent())
            node.getChildArray().append(newNode)

    def backPropagation(self, nodeToExplore, playerNo):
        tempNode = nodeToExplore
        while tempNode is not None:
            tempNode.getState().incrementVisit()
            if tempNode.getState().getPlayerNo() == playerNo:
                tempNode.getState().addScore(self.WIN_SCORE)
            tempNode = tempNode.getParent()

    def simulateRandomPlayout(self, node):
        tempNode = copy.deepcopy(node)
        # tempNode = node
        tempState = copy.deepcopy(tempNode.getState())
        boardStatus = tempState.getBoard().checkStatus()

        # print(self.opponent, ' == ', boardStatus)
        if boardStatus == self.opponent:
            tempNode.getParent().getState().setWinScore(-1 * sys.maxsize - 1)
            return boardStatus

        while boardStatus == -1:
            tempState.togglePlayer()
            tempState.randomPlay()
            boardStatus = tempState.getBoard().checkStatus()
        return boardStatus
