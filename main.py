from GAME_LOGIC.Board import Board
from MCTS.MonteCarloTreeSearch import MonteCarloTreeSearch

if __name__ == '__main__':
    print('hello world!')
    board = Board()
    player = Board.P1
    mcts = MonteCarloTreeSearch()

    board.printBoard()
    print("\n\n")
    while True:
        board = mcts.findNextMove(board, player)
        if board.checkStatus() == 1 or board.checkStatus() == 2:
            print("winner: ", board.checkStatus())
            break
        board.printBoard()
        print('')
        player = 3 - player

    winStatus = board.checkStatus()
    board.printBoard()
