import random

from GAME_LOGIC.Board import Board
from GAME_LOGIC.Position import Position


class State:
    def __init__(self, state=None, board=None):
        if state is not None:
            self.board = Board(state.getBoard())
            self.playerNo = state.getPlayerNo()
            self.visitCount = state.getVisitCount()
            self.winScore = state.getWinScore()
        elif board is not None:
            self.board = board
        else:
            self.board = Board()

    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board

    def getPlayerNo(self):
        return self.playerNo

    def setPlayerNo(self, playerNo):
        self.playerNo = playerNo

    def getOpponent(self):
        return 3 - self.playerNo

    def getVisitCount(self):
        return self.visitCount

    def setVisitCount(self, visitCount):
        self.visitCount = visitCount

    def getWinScore(self):
        return self.winScore

    def setWinScore(self, winScore):
        self.winScore = winScore

    def getAllPossibleStates(self):
        possibleStates = []
        availableMoves = self.board.getPossibleMoves(self.playerNo)
        for move in availableMoves:
            newState = State(self.board)
            newState.setPlayerNo(3 - self.playerNo)
            pos_from = Position(move[self.playerNo]['from'][0], move[self.playerNo]['from'][1])
            pos_to = Position(move[self.playerNo]['to'][0], move[self.playerNo]['to'][1])
            newState.getBoard().performMove(newState.getPlayerNo(), pos1=pos_from, pos2=pos_to)
            possibleStates.append(newState)
        return possibleStates

    def incrementVisit(self):
        self.visitCount += 1

    def addScore(self, score):
        # warning: overflow
        self.winScore += score

    def randomPlay(self):
        moves = self.board.getPossibleMoves(self.playerNo)  # pobranie listy dostępnych ruchów dla danego playerNo
        random_play = random.choice(moves)  # random.choice(moves)
        pos_from = Position(random_play[self.playerNo]['from'][0], random_play[self.playerNo]['from'][1])
        pos_to = Position(random_play[self.playerNo]['to'][0], random_play[self.playerNo]['to'][1])

        self.board.performMove(self.playerNo, pos1=pos_from, pos2=pos_to)  # wykonanie ruchu

    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo
