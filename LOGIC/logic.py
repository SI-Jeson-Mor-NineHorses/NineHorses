import random
import copy
from LOGIC.TreeNode import TreeNode, print_tree, save_tree, load_tree

def get_tuple(text):
    text = text[1:-1]
    out = text.split(', ')
    return int(out[0]), int(out[1])


class Thing:
    def __init__(self, color, y, x):
        self.color = color
        self.x = x
        self.y = y

    def gen_legal_moves(self, board):
        move_set = set()
        offsets = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                   (1, -2), (1, 2), (2, -1), (2, 1)]

        for offset in offsets:
            newX = self.x + offset[0]
            newY = self.y + offset[1]
            if self.move_check(self.color, newY, newX, board) and newX == 4 and newY == 4:
                move_set = set()
                move_set.add((newY, newX))
                return move_set
            if self.move_check(self.color, newY, newX, board):
                move_set.add((newY, newX))
        return move_set

    def move_check(self, your_color, y, x, board):
        if x < 0 or x > 8 or y < 0 or y > 8:
            return False
        piece = board[y][x]
        if piece.color == 'x':
            return True
        else:
            if piece.color != your_color:
                return True
            else:
                return False


class MCTS:
    def __init__(self):
        self.board = [
            [Thing("b", 0, i) for i in range(9)],
            [Thing("_", 1, x) for x in range(9)],
            [Thing("_", 2, x) for x in range(9)],
            [Thing("_", 3, x) for x in range(9)],
            [Thing("_", 4, x) for x in range(9)],
            [Thing("_", 5, x) for x in range(9)],
            [Thing("_", 6, x) for x in range(9)],
            [Thing("_", 7, x) for x in range(9)],
            [Thing("w", 8, i) for i in range(9)],
        ]

    def get_all_legal_moves(self, color, board):
        moves_list = []
        for i in board:
            for j in i:
                if j.color == color:
                    # automatyczne sugerowanie zakończenia gry
                    # if j.y == 4 and j.x == 4:
                    #     moves_list = []
                    #     for move in j.gen_legal_moves(board):
                    #         moves_list.append({color: {'from': (j.y, j.x), 'to': move}})
                    #         return moves_list
                    # else:
                    #     for move in j.gen_legal_moves(board):
                    #         if(move[0] == 4 and move[1] == 4):
                    #             moves_list = []
                    #             moves_list.append({color: {'from': (j.y, j.x), 'to': move}})
                    #             return moves_list
                    #         else:
                    #             moves_list.append({color: {'from': (j.y, j.x), 'to': move}})
                    for move in j.gen_legal_moves(board):
                        moves_list.append({color: {'from': (j.y, j.x), 'to': move}})
        return moves_list

    def move_piece(self, board, thing, y, x):
        board[y][x].color = thing.color
        board[thing.y][thing.x].color = '_' # Thing('_', thing.y, thing.x)

    def get_thing(self, board, x, y):
        return board[x][y]

    def simulate(self, start_player, root, board, time):
        simulation_tree = copy.deepcopy(root)
        while time:
            temp_board = copy.deepcopy(board)
            gameover = False  # flaga końca gry
            winner = ""  # identyfikator zwycięzcy
            player = start_player

            previous_move = ''
            current_move = ''
            current_node = simulation_tree  # ostatni dodany węzeł
            first_move_flag = 1  # flaga pierwszego ruchu
            try:
                while not gameover:
                    previous_move = current_move
                    if player == 1:
                        color = 'w'
                        all_player_moves = self.get_all_legal_moves(color,temp_board)
                        rand_move = random.randint(0, len(all_player_moves)-1)

                        y_from = all_player_moves[rand_move][color]['from'][0]
                        x_from = all_player_moves[rand_move][color]['from'][1]

                        y_to = all_player_moves[rand_move][color]['to'][0]
                        x_to = all_player_moves[rand_move][color]['to'][1]

                        piece = self.get_thing(temp_board, y_from, x_from)
                        # MCTS =============================================
                        # Przekazanie danych do drzewa
                        if first_move_flag: # pierwszy ruch w rozgrywce
                            node = TreeNode(player=color, _from='(%d, %d)' % (piece.y, piece.x), _to='(%d, %d)' % (y_to, x_to)) # inicjalizacja węzła
                            temp = simulation_tree.add_child(node) # dodanie węzła do korzenia drzewa
                            # zmiana obecnego węzła
                            if temp is not None:
                                current_node = temp
                            else:
                                current_node = node
                            first_move_flag = 0
                        else:  # kolejny ruch w rozgrywce
                            node = TreeNode(player=color, _from='(%d, %d)' % (piece.y, piece.x), _to='(%d, %d)' % (y_to, x_to))  # inicjalizacja węzła
                            temp = current_node.add_child(node)  # dodanie węzła do obecnego (poprzedniego) węzła
                            # zmiana obecnego węzła
                            if temp is not None:
                                current_node = temp
                            else:
                                current_node = node
                        # ===================================================
                        self.move_piece(temp_board, piece, y_to, x_to)
                        player = 2

                    elif player == 2:
                        color = 'b'
                        all_player_moves = self.get_all_legal_moves(color,temp_board)
                        rand_move = random.randint(0, len(all_player_moves)-1)

                        y_from = all_player_moves[rand_move][color]['from'][0]
                        x_from = all_player_moves[rand_move][color]['from'][1]

                        y_to = all_player_moves[rand_move][color]['to'][0]
                        x_to = all_player_moves[rand_move][color]['to'][1]

                        piece = self.get_thing(temp_board, y_from, x_from)
                        # MCTS =============================================
                        # Przekazanie danych do drzewa
                        if first_move_flag: # pierwszy ruch w rozgrywce
                            node = TreeNode(player=color, _from='(%d, %d)' % (piece.y, piece.x), _to='(%d, %d)' % (y_to, x_to)) # inicjalizacja węzła
                            temp = simulation_tree.add_child(node) # dodanie węzła do korzenia drzewa
                            # zmiana obecnego węzła
                            if temp is not None:
                                current_node = temp
                            else:
                                current_node = node
                            first_move_flag = 0
                        else:  # kolejny ruch w rozgrywce
                            node = TreeNode(player=color, _from='(%d, %d)' % (piece.y, piece.x), _to='(%d, %d)' % (y_to, x_to))  # inicjalizacja węzła
                            temp = current_node.add_child(node)  # dodanie węzła do obecnego (poprzedniego) węzła
                            # zmiana obecnego węzła
                            if temp is not None:
                                current_node = temp
                            else:
                                current_node = node
                        # ===================================================
                        self.move_piece(temp_board, piece, y_to, x_to)
                        player = 1

                    arr = []
                    for i in range(9):
                        for piecee in temp_board[i]:
                            # print(piecee.color, end='')
                            # print('(',piecee.y,piecee.x,': ',piecee.color,')',end='')
                            arr.append(piecee.color)
                    #     print('')
                    # print('')

                    # check end game
                    if 'w' not in arr:
                        gameover = True
                        winner = "Black"
                    elif 'b' not in arr:
                        gameover = True
                        winner = "White"

                    current_move = arr[40]
                    if previous_move == 'w' and current_move == "_":
                        gameover = True
                        winner = "White"
                    elif previous_move == 'b' and current_move == "_":
                        gameover = True
                        winner = "Black"
            except Exception as e:
                print('Exception: ',e)
                # pass
            # print(winner)
            current_node.update_score(winner[0].lower())
            # print_tree(root)
            time -= 1
        best = simulation_tree.children[0]
        for x in simulation_tree.children:
            if x.score > best.score:
                best = x
        return best

def simplify_board(input_board):
    output_board = [[Thing(i.color, i.y, i.x) for i in j ]for j in input_board]
    return output_board

if __name__ == "__main__":
    main_board = [
        [Thing("b", 0, i) for i in range(9)],
        [Thing("_", 1, x) for x in range(9)],
        [Thing("_", 2, x) for x in range(9)],
        [Thing("_", 3, x) for x in range(9)],
        [Thing("_", 4, x) for x in range(9)],
        [Thing("_", 5, x) for x in range(9)],
        [Thing("_", 6, x) for x in range(9)],
        [Thing("_", 7, x) for x in range(9)],
        [Thing("w", 8, i) for i in range(9)],
    ]
    mcts = MCTS()
    tree = TreeNode(name='ROOT',n_plays=1,n_wins=1, children=[])
    next = mcts.simulate(2, tree, main_board, 1000)
    # save_tree(tree)
    # print_tree(tree)
    print("BEST: ", next.score, '=', next.n_wins, '/', next.n_plays, next.name)
