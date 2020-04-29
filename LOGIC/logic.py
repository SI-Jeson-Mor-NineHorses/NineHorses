def check_gameover(arr, previous_move):
    winner = ""

    # check end game
    if 'wN' not in arr:
        winner = "Black"
    elif 'bN' not in arr:
        winner = "White"

    current_move = arr[40]
    if previous_move == 'wN' and current_move == "_N":
        winner = "White"
    elif previous_move == 'bN' and current_move == "_N":
        winner = "Black"
    return winner
