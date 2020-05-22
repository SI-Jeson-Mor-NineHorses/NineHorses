from LOGIC.pieces import *


class Board:
    # Plansza reprezentowana za pomocą tablicy 9x9. 'None' oznacza pusty kwadrat.
    def __init__(self):
        self.recently_highlighted = []
        self.empty = [[None for x in range(9)] for y in range(9)]
        self.array = [
            [Knight("b", 0, i) for i in range(9)],
            [Empty("_", 1, x) for x in range(9)],
            [Empty("_", 2, x) for x in range(9)],
            [Empty("_", 3, x) for x in range(9)],
            [Empty("_", 4, x) for x in range(9)],
            [Empty("_", 5, x) for x in range(9)],
            [Empty("_", 6, x) for x in range(9)],
            [Empty("_", 7, x) for x in range(9)],
            [Knight("w", 8, i) for i in range(9)],
        ]

    def get_all_legal_moves(self, color):
        moves_list = []
        for i in self.array:
            for j in i:
                if j.color == color:
                    for move in j.gen_legal_moves(self):
                        moves_list.append({color: {'from': (j.y, j.x), 'to': move}})
        return moves_list


    def move_piece(self, piece, y, x):
        oldx = piece.x
        oldy = piece.y
        piece.x = x
        piece.y = y
        piece.rect.x = x * 60
        piece.rect.y = y * 60
        self.array[oldy][oldx] = Empty('_', oldy, oldx)

        self.array[y][x] = piece
        piece.unhighlight()

    def get_piece(self, x, y):
        return self.array[y][x]

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

    # podświetlenie opcjonalnych ruchów
    def highlight_optional_moves(self, moves):
        self.recently_highlighted = moves
        for x in moves:
            self.array[x[0]][x[1]].highlight()

    # usunięcie podświetlenia opcjonalnych ruchów
    def unhighlight_optional_moves(self):
        for x in self.recently_highlighted:
            self.array[x[0]][x[1]].unhighlight()
