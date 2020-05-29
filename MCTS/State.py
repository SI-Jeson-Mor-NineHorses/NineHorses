from GAME_LOGIC.Board import Board


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
            board = Board()

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

    # TODO: zmiana logiki na nine horses w getAllPossibleStates
    def getAllPossibleStates(self):
        possibleStates = []
        availablePositions = self.board.getEmptyPositons

    def incrementVisit(self):
        self.visitCount += 1

    def addScore(self, score):
        # warning: overflow
        self.winScore += score

    # TODO: zmiana logiki na nine horses w randomPlay
    def randomPlay(self):
        pass
        # 1 pobranie listy dostępnych ruchów dla danego playerNo
        # 2 random.choice(self.movesArray)
        # 3 preform move

    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo
