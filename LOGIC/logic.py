import random
import time
import copy
from LOGIC.TreeNode import TreeNode, print_tree, save_tree, load_tree, print_children_tree

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

    def run_search(self, color, board, root, timeout):
        search_root = copy.deepcopy(root)
        temp_board = copy.deepcopy(board)

        if color == 'w':
            player = 1
        else:
            player = 2
        current_root = search_root

        current_N = 30

        begin = time.time()
        end = time.time() + timeout
        while time.time() < end:
            # print(current_root.children)
            # print(current_root.n_plays, current_root.name)
            # print("N = ", current_N)
            if current_root.children.__len__() == 0:
                # print("add children")
                legal_moves = self.get_all_legal_moves(color, temp_board)

                for i in range(len(legal_moves)):
                    y_from = legal_moves[i][color]['from'][0]
                    x_from = legal_moves[i][color]['from'][1]

                    y_to = legal_moves[i][color]['to'][0]
                    x_to = legal_moves[i][color]['to'][1]

                    node = TreeNode(player=color, _from='(%d, %d)' % (y_from, x_from),
                                    _to='(%d, %d)' % (y_to, x_to), parent = current_root)  # inicjalizacja węzła
                    # print(node)
                    current_root.add_child(node)  # dodanie węzła do obecnego (poprzedniego) węzła
                    # print(current_root)
                    temp_board = copy.deepcopy(temp_board)
                    temp_thing = self.get_thing(temp_board, y_from, x_from)
                    self.move_piece(temp_board, temp_thing, y_to, x_to)
                    result = self.raw_simulation(player, node, temp_board)
                    node.update_score(result)
                    current_root.is_expanded = True
                    # current_N = len(legal_moves)

            elif current_root.children.__len__() > 0: #and current_root.n_plays <= current_N: # 30
                best_node = current_root.children[0]
                for node in current_root.children:
                    if node.is_expanded == False:
                        if node.score > best_node.score:
                            best_node = node

                # print(best_node.n_plays)
                if best_node.n_plays >= 20:
                    # print("reset")
                    current_root = search_root
                    temp_board = copy.deepcopy(board)
                else:
                    # current_root = best_node
                    current_root_move_from = get_tuple(best_node.move_from)
                    current_root_move_to = get_tuple(best_node.move_to)

                    temp_board = copy.deepcopy(temp_board)
                    temp_thing = self.get_thing(temp_board, current_root_move_from[0], current_root_move_from[1])
                    self.move_piece(temp_board, temp_thing, current_root_move_to[0], current_root_move_to[1])
                    result = self.raw_simulation(1, best_node, temp_board)
                    best_node.update_score(result)

                # print(current_root.n_plays)
                # print('select best children')
                # all_expanded = 0
                # best_node = current_root.children[0]
                # print(best_node.n_plays)
                # for node in current_root.children:
                #     if node.is_expanded == False:
                #         all_expanded += 1
                #     if node.n_plays < current_N:
                #         if node.score > best_node.score:
                #             if node.is_expanded == False:
                #                 best_node = node
                #
                #             if node.n_plays == 1:
                #                 best_node = node
                #                 break

                # if all_expanded > 0:
                #     current_root = search_root
                #     temp_board = copy.deepcopy(board)
                # else:
                #     current_root = best_node
                #                 #     current_root_move_from = get_tuple(current_root.move_from)
                #                 #     current_root_move_to = get_tuple(current_root.move_to)
                #                 #
                #                 #     temp_board = copy.deepcopy(temp_board)
                #                 #     temp_thing = self.get_thing(temp_board, current_root_move_from[0], current_root_move_from[1])
                #                 #     self.move_piece(temp_board, temp_thing, current_root_move_to[0], current_root_move_to[1])
                #                 #     result = self.raw_simulation(1, current_root, temp_board)
                #                 #     current_root.update_score(result)

            elif current_root.n_plays >current_N:
                print("reset")
                current_root = search_root
                temp_board = copy.deepcopy(board)


        for child in search_root.children:
            child.score = child.calc_UCB1(1.4)
        return search_root




    def get_all_legal_moves(self, color, board):
        moves_list = []
        for i in board:
            for j in i:
                if j.color == color:
                    for move in j.gen_legal_moves(board):
                        moves_list.append({color: {'from': (j.y, j.x), 'to': move}})
        return moves_list

    def move_piece(self, board, thing, y, x):
        board[y][x].color = thing.color
        board[thing.y][thing.x].color = '_' # Thing('_', thing.y, thing.x)

    def get_thing(self, board, y, x):
        return board[y][x]

    def raw_simulation(self, player, root, board):
        simulation_tree = copy.deepcopy(root)
        temp_board = copy.deepcopy(board)
        gameover = False  # flaga końca gry
        winner = "_"  # identyfikator zwycięzcy
        player = player

        previous_move = '_'
        current_move = board[4][4].color  # inicjalizacja aktualnego stanu środka
        current_node = simulation_tree  # ostatni dodany węzeł
        first_move_flag = 1  # flaga pierwszego ruchu
        try:
            while not gameover:
                previous_move = current_move
                if player == 1:
                    color = 'w'
                    all_player_moves = self.get_all_legal_moves(color, temp_board)
                    rand_move = random.randint(0, len(all_player_moves) - 1)

                    y_from = all_player_moves[rand_move][color]['from'][0]
                    x_from = all_player_moves[rand_move][color]['from'][1]

                    y_to = all_player_moves[rand_move][color]['to'][0]
                    x_to = all_player_moves[rand_move][color]['to'][1]

                    piece = self.get_thing(temp_board, y_from, x_from)
                    # MCTS =============================================
                    # Przekazanie danych do drzewa
                    if first_move_flag:  # pierwszy ruch w rozgrywce
                        node = TreeNode(player=color, _from='(%d, %d)' % (piece.y, piece.x),
                                        _to='(%d, %d)' % (y_to, x_to))  # inicjalizacja węzła
                        temp = simulation_tree.add_child(node)  # dodanie węzła do korzenia drzewa
                        # zmiana obecnego węzła
                        if temp is not None:
                            current_node = temp
                        else:
                            current_node = node
                        first_move_flag = 0
                    else:  # kolejny ruch w rozgrywce
                        node = TreeNode(player=color, _from='(%d, %d)' % (piece.y, piece.x),
                                        _to='(%d, %d)' % (y_to, x_to))  # inicjalizacja węzła
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
                    all_player_moves = self.get_all_legal_moves(color, temp_board)
                    rand_move = random.randint(0, len(all_player_moves) - 1)

                    y_from = all_player_moves[rand_move][color]['from'][0]
                    x_from = all_player_moves[rand_move][color]['from'][1]

                    y_to = all_player_moves[rand_move][color]['to'][0]
                    x_to = all_player_moves[rand_move][color]['to'][1]

                    piece = self.get_thing(temp_board, y_from, x_from)
                    # MCTS =============================================
                    # Przekazanie danych do drzewa
                    if first_move_flag:  # pierwszy ruch w rozgrywce
                        node = TreeNode(player=color, _from='(%d, %d)' % (piece.y, piece.x),
                                        _to='(%d, %d)' % (y_to, x_to))  # inicjalizacja węzła
                        temp = simulation_tree.add_child(node)  # dodanie węzła do korzenia drzewa
                        # zmiana obecnego węzła
                        if temp is not None:
                            current_node = temp
                        else:
                            current_node = node
                        first_move_flag = 0
                    else:  # kolejny ruch w rozgrywce
                        node = TreeNode(player=color, _from='(%d, %d)' % (piece.y, piece.x),
                                        _to='(%d, %d)' % (y_to, x_to))  # inicjalizacja węzła
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
                        arr.append(piecee.color)

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
            print('Exception: ', e)

        winner = winner[0].lower()
        if root.player == winner:
            return winner


    def simulate(self, start_player, root, board, time, output_number=1):
        simulation_tree = copy.deepcopy(root)
        while time:
            temp_board = copy.deepcopy(board)
            gameover = False  # flaga końca gry
            winner = ""  # identyfikator zwycięzcy
            player = start_player

            previous_move = '_'
            # print(board[4][4].color)
            current_move = board[4][4].color # inicjalizacja aktualnego stanu środka

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
        # print_children_tree(simulation_tree)
        # print_tree(simulation_tree)
        if output_number == 1:
            best = simulation_tree.children[0]
            for x in simulation_tree.children:
                if x.score > best.score:
                    best = x
            return [best]
        else:
            temp_dict = {}
            best_nodes = []
            for x in simulation_tree.children:
                temp_dict[x.name]=x.score
            sorted_x = list(reversed(list({k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1])})))[0:output_number]
            for x in simulation_tree.children:
                for y in sorted_x:
                    if x.name == y:
                        best_nodes.append(x)
            return best_nodes

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
    main_board[6][3].color = 'w'
    main_board[8][0].color = '_'
    # main_board[5][6].color = 'b'

    mcts = MCTS()
    tree = TreeNode(name='ROOT', n_plays=0, n_wins=0, children=[])
    output = mcts.run_search('b',main_board, tree, 10)
    best = TreeNode(name="XD", n_plays=0, n_wins=0, score = 0, children=[])
    for i in output.children:
        if i.n_plays is not 1:
            if i.score > best.score:
                best = i
    print(best.name, best.score)
    # print(output.n_plays)
    print_children_tree(output)
    # print_tree(output)
    # par = TreeNode(name='b:(6, 3)=>(4, 2)', _from='(6, 3)', _to='(4, 2)', player='b', n_plays=1, n_wins=0, score=1.0)
    # center = TreeNode(name='w:(6, 3)=>(4, 4)', _from='(6, 3)', _to='(4, 4)', player='w', n_plays=1, n_wins=0, score=1.0)
    # center.add_child(par)
    # tree.add_child(center)
    #
    #
    # next = mcts.simulate(1, tree, main_board, 1000, 5)
    # for n in next:
    #     print("TOP: ", n.score, '=', n.n_wins, '/', n.n_plays, n.name)
    #
    # # next = mcts.simulate(1, tree, main_board, 1)
    # # print("BEST: ", next.score, '=', next.n_wins, '/', next.n_plays, next.name)
