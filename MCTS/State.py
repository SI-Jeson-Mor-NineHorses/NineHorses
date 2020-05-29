import copy
import random
import sys

from GAME_LOGIC.Board import Board
from GAME_LOGIC.Position import Position


class State:
    visitCount = 0
    winScore = 0

    def __init__(self, state=None, board=None):
        self.score = 0
        self.move_from = None
        self.move_to = None
        if state is not None:
            self.board = Board(board=state.getBoard())
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
        player = 3 - self.playerNo
        availableMoves = self.board.getPossibleMoves(player)
        for move in availableMoves:
            newState = State(board=copy.deepcopy(self.board))
            newState.setPlayerNo(player)
            pos_from = Position(y=move[player]['from'][0], x=move[player]['from'][1])
            pos_to = Position(y=move[player]['to'][0], x=move[player]['to'][1])
            newState.move_from = pos_from
            newState.move_to = pos_to
            newState.getBoard().performMove(newState.getPlayerNo(), pos1=pos_from, pos2=pos_to)
            possibleStates.append(newState)
        return possibleStates

    def incrementVisit(self):
        self.visitCount += 1

    def addScore(self, score):
        if self.winScore != -1 * sys.maxsize - 1:
            self.winScore += score

    def randomPlay(self):
        moves = self.board.getPossibleMoves(self.playerNo)  # pobranie listy dostępnych ruchów dla danego playerNo
        out_moves = []
        for m in moves:
            if m[self.playerNo]['from'][0] == 4 and m[self.playerNo]['from'][1] == 4:
                out_moves.append(m)
        # if len(out_moves) > 0:
        #     # print('out')
        #     random_play = random.choice(out_moves)
        # else:
        random_play = random.choice(moves)  # random.choice(moves)
        pos_from = Position(y=random_play[self.playerNo]['from'][0], x=random_play[self.playerNo]['from'][1])
        pos_to = Position(y=random_play[self.playerNo]['to'][0], x=random_play[self.playerNo]['to'][1])
        # self.move_from = pos_from
        # self.move_to = pos_to
        self.board.performMove(self.playerNo, pos1=pos_from, pos2=pos_to)  # wykonanie ruchu

    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo
