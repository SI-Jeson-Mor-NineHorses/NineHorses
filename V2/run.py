from V2.GAME_LOGIC.Board import Board
from V2.MCTS.MonteCarloTreeSearch import MonteCarloTreeSearch

if __name__ == '__main__':
    '''
    Console MCTS-like NineHorses Simulation
    '''
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
