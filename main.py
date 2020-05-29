from GAME_LOGIC.Board import Board
from MCTS.MonteCarloTreeSearch import MonteCarloTreeSearch

if __name__ == '__main__':
    print('hello world!')
    board = Board()
    player = Board.P1
    mcts = MonteCarloTreeSearch()

    while True:
        board = mcts.findNextMove(board, player)
        if board.checkStatus() != -1:
            break
        player = 3 - player

    winStatus = board.checkStatus()
    board.printBoard()
