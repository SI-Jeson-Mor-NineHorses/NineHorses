from LOGIC.pieces import *

class Board:
    # Plansza reprezentowana za pomocą tablicy 9x9. 'None' oznacza pusty kwadrat.

    def __init__(self):
        self.empty = [[None for x in range(9)] for y in range(9)]
        self.array = [
            [Knight("b", 0, i) for i in range(9)],
            [None for x in range(9)],
            [None for x in range(9)],
            [None for x in range(9)],
            [None for x in range(9)],
            [None for x in range(9)],
            [None for x in range(9)],
            [None for x in range(9)],
            [Knight("w", 8, i) for i in range(9)],
        ]

    def move_piece(self, piece, y, x):
        oldx = piece.x
        oldy = piece.y
        piece.x = x
        piece.y = y
        piece.rect.x = x * 60
        piece.rect.y = y * 60
        self.array[oldy][oldx] = None

        self.array[y][x] = piece
        piece.unhighlight()

    # Wypisanie tablicy planszy do konsoli

    def print_to_terminal(self):
        for j in range(9):
            arr = []
            for piece in self.array[j]:
                if piece != None:
                    arr.append(piece.color + piece.symbol)
                else:
                    arr.append("--")
            print(arr)


