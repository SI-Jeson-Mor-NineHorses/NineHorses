# TODO: MonteCarloTreeSearch class
from TREE import Tree
from TREE import Node
from MCTS import UCT
from GAME_LOGIC import Board
import time
import copy
import sys


class MonteCarloTreeSearch:
    def __init__(self):
        self.level = 3
        self.WIN_SCORE = 10
        self.opponent = 0

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def getMillisForCurrentLevel(self):
        return 2 * (self.level - 1) + 1

    def findNextMove(self, board, playerNo, root):
        start = int(round(time.time() * 1000))
        end = start + 60 * self.getMillisForCurrentLevel()

        self.opponent = 3 - playerNo
        tree = Tree.Tree()
        rootNode = tree.getRoot()
        rootNode.getState().setBoard(board)
        rootNode.getState().setPlayerNo(self.opponent)

        while int(round(time.time() * 1000)) < end:
            #Phase 1 - Selection
            promisingNode = self.selectPromisingNode(rootNode)

            #Phase 2 - Expansion
            if promisingNode.getState().getBoard().checkStatus() == board.IN_PROGRESS:
                self.expandNode(promisingNode)

            #Phase 3 - Simulation
            nodeToExplore = promisingNode
            if len(promisingNode.getChildArray()) > 0:
                nodeToExplore = promisingNode.getRandomChildNode()

            playoutResult = self.simulateRandomPlayout(nodeToExplore)

            #Phase 4 - Update

            self.backPropagation(nodeToExplore, playoutResult)

        winnerNode = rootNode.getChildWithMaxScore()
        tree.setRoot(winnerNode)
        return winnerNode.getState.getBoard()

    def selectPromisingNode(self, rootNode):
        node = copy.deepcopy(rootNode)
        while len(node.getChildArray()) != 0:
            node = UCT.findBestNodeWithUCT(node)

        return node

    def expandNode(self, node):
        possibleStates = node.getState().getAllPossibleStates()
        for state in possibleStates:
            newNode = Node(state=state)
            newNode.setParent(node)
            newNode.getState().setPlayerNo(node.getState().getOpponent())
            node.getChildArray().add(newNode)

    def backPropagation(self, nodeToExplore, playerNo):
        tempNode = copy.deepcopy(nodeToExplore)
        while tempNode != None:
            tempNode.getState().incrementVisit()
            if tempNode.getState().getPlayerNo() == playerNo:
                tempNode.getState().addScore(self.WIN_SCORE)
            tempNode = tempNode.getParent()

    def simulateRandomPlayout(self, node):
        tempNode = copy.deepcopy(Node(node = node))
        tempState = copy.deepcopy(tempNode.getState())
        boardStatus = tempState.getBoard().checkStatus()

        if boardStatus == self.opponent:
            tempNode.getParent().getState().setWinScore(-1 * sys.maxsize - 1)
            return boardStatus

        while boardStatus == Board.IN_PROGRESS:
            tempState.togglePlayer()
            tempState.randomPlay()
            boardStatus = tempState.getBoard().checkStatus()

        return boardStatus
