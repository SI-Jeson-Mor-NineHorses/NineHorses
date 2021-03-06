import pygame
import sys
from MAIN.LOGIC.logic import *
from MAIN.LOGIC.TreeNode import TreeNode, print_tree, save_tree, load_tree
from MAIN.LOGIC.board import *

pygame.init()
pygame.font.init()

# Ustawienia okna gry
screen = pygame.display.set_mode((800, 60 * 9))
pygame.display.set_caption('Python Jeson Mor Game')
clock = pygame.time.Clock()  # odświeżanie okna

# Załadowanie wygerowanej planszy
bg = pygame.image.load("../MAIN/assets/board.png").convert()
player = 1

board = Board()

global all_sprites_list, sprites
all_sprites_list = pygame.sprite.Group()
sprites = [piece for row in board.array for piece in row if piece]
all_sprites_list.add(sprites)


def reload_sprites():
    return [piece for row in board.array for piece in row if piece]

def select_piece_xy(color, x, y):
    # get a list of all sprites that are under the mouse cursor
    # lista wszystkich duszków, ktore sa pod kursorem myszy
    clicked_sprites = [s for s in sprites if s.x == x and s.y == y]

    # podświetla i zwaraca jeśli jest to pionek gracza
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        clicked_sprites[0].highlight()
        return clicked_sprites[0]
    elif len(clicked_sprites) == 1:
        return clicked_sprites[0]

def select_piece(color):
    pos = pygame.mouse.get_pos()
    # get a list of all sprites that are under the mouse cursor
    # lista wszystkich duszków, ktore sa pod kursorem myszy
    clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]

    # podświetla i zwaraca jeśli jest to pionek gracza
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        clicked_sprites[0].highlight()
        return clicked_sprites[0]
    elif len(clicked_sprites) == 1:
        return clicked_sprites[0]


def select_square():
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = y // 60
    return y, x

# mode:
# 0 - gracz vs gracz
# 1 - gracz vs komputer
# 2 - komputer vs komputer+
def run_game(game_tree, mode):
    global sprites
    gameover = False # flaga końca gry
    winner = "" # identyfikator zwycięzcy
    selected = False
    trans_table = dict()
    checkWhite = False
    player = 1

    previous_move = ''
    current_move = ''

    first_move_flag = 1 # flaga pierwszego ruchu
    current_node = game_tree # ostatni dodany węzeł
    copy_current_node = copy.deepcopy(current_node)
    run_flag = 0


    while not gameover:
        previous_move = current_move
        if player == 1 and run_flag == 1:
            if mode == 0 or mode == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    # wybór pionka do wykonania ruchu
                    elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                        board.unhighlight_optional_moves()
                        piece = select_piece("w")

                        # generuje "legalne" ruchy pionka
                        if piece != Empty and piece.color == "w":
                            # sprawdzenie dostępnych ruchów
                            player_moves = piece.gen_legal_moves(board)
                            # all_player_moves = board.get_all_legal_moves("w")

                            # podświetlenie dostępnych ruchów
                            board.highlight_optional_moves(player_moves)
                            selected = True

                    # pionek wybrany -> wybór ruchu
                    elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                        board.unhighlight_optional_moves()
                        square = select_square()

                        # sprawdza czy wybrane pole jest w zasięgu dozwolonych ruchów
                        if square in player_moves:
                            oldx = piece.x
                            oldy = piece.y
                            dest = board.array[square[0]][square[1]]

                            # MCTS =============================================
                            # Przekazanie danych do drzewa
                            if first_move_flag: # pierwszy ruch w rozgrywce
                                node = TreeNode(player='w', _from='(%d, %d)' % (piece.y, piece.x), _to='(%d, %d)' % (square[0], square[1])) # inicjalizacja węzła
                                temp = game_tree.add_child(node) # dodanie węzła do korzenia drzewa
                                # zmiana obecnego węzła
                                if temp is not None:
                                    current_node = temp
                                else:
                                    current_node = node
                                first_move_flag = 0
                            else:  # kolejny ruch w rozgrywce
                                node = TreeNode(player='w', _from='(%d, %d)' % (piece.y, piece.x), _to='(%d, %d)' % (square[0], square[1])) # inicjalizacja węzła
                                temp = current_node.add_child(node) # dodanie węzła do obecnego (poprzedniego) węzła
                                # zmiana obecnego węzła
                                if temp is not None:
                                    current_node = temp
                                else:
                                    current_node = node
                            #===================================================

                            # wykonanie ruchu
                            board.move_piece(piece, square[0], square[1])

                            if dest:  # aktualizacja 'duszków' względem stanu planszy
                                sprites = reload_sprites()
                                all_sprites_list.empty()
                                all_sprites_list.add(sprites)

                            selected = False
                            player = 2

                        # anuluje ruch, jezeli wybrane zostalo to samo pole
                        elif (piece.y, piece.x) == square:
                            piece.unhighlight()
                            selected = False

                        # ruch jest nieważny
                        else:
                            pygame.display.update()
                            # board.highlight_optional_moves(player_moves)
                            pygame.time.wait(1000)
            elif mode == 2:
                #TODO: zmienić kryteria wyboru ruchu (drzewo vs symulacja)

                # if current_node.n_plays>=10:
                #     # możemy brać wszystkie albo zrobić symulacje i wybrać 5 obiecujących
                #     mcts = MCTS()
                #     input_board = simplify_board(board.array)
                #     expansion_moves = mcts.simulate(1, current_node, input_board, 1000, 5)
                #     for child in expansion_moves:
                #         y_from = get_tuple(child.move_from)[0]
                #         x_from = get_tuple(child.move_from)[1]
                #
                #         y_to = get_tuple(child.move_to)[0]
                #         x_to = get_tuple(child.move_to)[1]
                #
                #         node = TreeNode(player='w', _from='(%d, %d)' % (y_from, x_from),
                #                         _to='(%d, %d)' % (y_to, x_to))  # inicjalizacja węzła
                #         temp = current_node.add_child(node)  # dodanie węzła do obecnego (poprzedniego) węzła

                if current_node.children.__len__() > 0: # węzeł ma dzieci (nie jest liściem)
                    best_move = None
                    best_moves = []
                    for next in current_node.children:
                        if best_move == None:
                            best_move = next
                            best_moves = [best_move]
                        elif next.score > best_move.score:
                            best_move = next
                        elif next.score == best_move.score:
                            best_moves.append(next)
                    if len(best_moves) > 1:
                        best_move = best_moves[random.randint(0,len(best_moves)-1)]

                    move_from = get_tuple(best_move.move_from)
                    move_to = get_tuple(best_move.move_to)

                    piece = select_piece_xy("w", move_from[1], move_from[0])

                    square = (move_to[0], move_to[1])


                    dest = board.array[move_to[0]][move_to[1]]
                    # MCTS =============================================
                    # Przekazanie danych do drzewa
                    node = TreeNode(player='w', _from='(%d, %d)' % (piece.y, piece.x),
                                    _to='(%d, %d)' % (square[0], square[1]))  # inicjalizacja węzła
                    # if current_node.n_plays >= 30:
                    temp = current_node.add_child(node)  # dodanie węzła do obecnego (poprzedniego) węzła
                    # zmiana obecnego węzła
                    if temp is not None:
                        current_node = temp
                    else:
                        current_node = node
                    # ===================================================
                    board.move_piece(piece, move_to[0], move_to[1]) # wykonanie ruchu
                    if dest:
                        sprites = reload_sprites()
                        all_sprites_list.empty()
                        all_sprites_list.add(reload_sprites())
                    player = 2

                else: # węzeł jest liściem
                    mcts = MCTS()
                    input_board = simplify_board(board.array)
                    #TODO: symulacje przeprowadzić na osobnym wątku tak aby nie blokowała pętli gui
                    print(current_node.name)
                    next = mcts.simulate(1, current_node, input_board, 1000)[0]
                    print("BEST w: ", next.score, '=', next.n_wins, '/', next.n_plays, next.name)

                    y_from = get_tuple(next.move_from)[0]
                    x_from = get_tuple(next.move_from)[1]

                    y_to = get_tuple(next.move_to)[0]
                    x_to = get_tuple(next.move_to)[1]

                    piece = select_piece_xy("w", x_from, y_from)
                    square = (y_to, x_to)


                    dest = board.array[y_to] [x_to]

                    # MCTS =============================================
                    # Przekazanie danych do drzewa
                    if first_move_flag:  # pierwszy ruch w rozgrywce
                        node = TreeNode(player='w', _from='(%d, %d)' % (piece.y, piece.x),
                                        _to='(%d, %d)' % (square[0], square[1]))  # inicjalizacja węzła

                        temp = game_tree.add_child(node)  # dodanie węzła do korzenia drzewa
                        # zmiana obecnego węzła
                        if temp is not None:
                            current_node = temp
                        else:
                            current_node = node
                        first_move_flag = 0
                    else:
                        node = TreeNode(player='w', _from='(%d, %d)' % (piece.y, piece.x),
                                        _to='(%d, %d)' % (square[0], square[1])) # inicjalizacja węzła
                        # if current_node.n_plays >= 30:
                        temp = current_node.add_child(node) # dodanie węzła do obecnego (poprzedniego) węzła
                        # zmiana obecnego węzła
                        if temp is not None:
                            current_node = temp
                        else:
                            current_node = node
                    # ===================================================

                    # print(y_to,x_to)
                    board.move_piece(piece, y_to, x_to) # wykonanie ruchu
                    if dest:
                        sprites = reload_sprites()
                        all_sprites_list.empty()
                        all_sprites_list.add(reload_sprites())

                    player=2
                pygame.display.update()
                pygame.time.wait(1000)


        # drugi gracz
        elif player == 2 and run_flag == 1:
            if mode == 1 or mode == 2:
                # if current_node.n_plays >= 10:
                #     pass
                    # # możemy brać wszystkie albo zrobić symulacje i wybrać 5 obiecujących
                    # mcts = MCTS()
                    # input_board = simplify_board(board.array)
                    # expansion_moves = mcts.simulate(2, current_node, input_board, 1000, 5)
                    # for child in expansion_moves:
                    #     y_from = get_tuple(child.move_from)[0]
                    #     x_from = get_tuple(child.move_from)[1]
                    #
                    #     y_to = get_tuple(child.move_to)[0]
                    #     x_to = get_tuple(child.move_to)[1]
                    #
                    #     node = TreeNode(player='b', _from='(%d, %d)' % (y_from, x_from),
                    #                     _to='(%d, %d)' % (y_to, x_to))  # inicjalizacja węzła
                    #     temp = current_node.add_child(node)  # dodanie węzła do obecnego (poprzedniego) węzła

                if current_node.children.__len__() > 0: # węzeł ma dzieci (nie jest liściem)
                    best_move = None
                    best_moves = []
                    for next in current_node.children:
                        if best_move == None:
                            best_move = next
                            best_moves = [best_move]
                        elif next.score > best_move.score:
                            best_move = next
                        elif next.score == best_move.score:
                            best_moves.append(next)
                    if len(best_moves) > 1:
                        best_move = best_moves[random.randint(0, len(best_moves)-1)]
                    move_from = get_tuple(best_move.move_from)
                    move_to = get_tuple(best_move.move_to)

                    piece = select_piece_xy("b", move_from[1], move_from[0])

                    square = (move_to[0], move_to[1])

                    dest = board.array[move_to[0]][move_to[1]]

                    # MCTS =============================================
                    # Przekazanie danych do drzewa
                    node = TreeNode(player='b', _from='(%d, %d)' % (piece.y, piece.x),
                                    _to='(%d, %d)' % (square[0], square[1]))  # inicjalizacja węzła

                    temp = current_node.add_child(node)  # dodanie węzła do obecnego (poprzedniego) węzła
                    # zmiana obecnego węzła
                    if temp is not None:
                        current_node = temp
                    else:
                        current_node = node
                    # ===================================================

                    board.move_piece(piece, move_to[0], move_to[1]) # wykonanie ruchu
                    if dest:
                        sprites = reload_sprites()
                        all_sprites_list.empty()
                        all_sprites_list.add(reload_sprites())
                    player = 1

                else: # węzeł jest liściem
                    mcts = MCTS()
                    input_board = simplify_board(board.array)
                    print(current_node.name)
                    next = mcts.simulate(2, current_node, input_board, 1000)[0]
                    print("BEST b: ", next.score, '=', next.n_wins, '/', next.n_plays, next.name)

                    y_from = get_tuple(next.move_from)[0]
                    x_from = get_tuple(next.move_from)[1]

                    y_to = get_tuple(next.move_to)[0]
                    x_to = get_tuple(next.move_to)[1]

                    piece = select_piece_xy("b", x_from, y_from)
                    square = (y_to, x_to)

                    dest = board.array[y_to] [x_to]
                    # print(dest)

                    # MCTS =============================================
                    # Przekazanie danych do drzewa
                    node = TreeNode(player='b', _from='(%d, %d)' % (piece.y, piece.x), _to='(%d, %d)' % (square[0], square[1])) # inicjalizacja węzła
                    # if current_node.n_plays >= 30:
                    temp = current_node.add_child(node) # dodanie węzła do obecnego (poprzedniego) węzła
                    # zmiana obecnego węzła
                    if temp is not None:
                        current_node = temp
                    else:
                        current_node = node
                    # ===================================================
                    # print(y_to,x_to)
                    board.move_piece(piece, y_to, x_to) # wykonanie ruchu
                    if dest:
                        sprites = reload_sprites()
                        all_sprites_list.empty()
                        all_sprites_list.add(reload_sprites())
                    player=1

                pygame.display.update()
                pygame.time.wait(1000)

            elif mode == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                        board.unhighlight_optional_moves()
                        piece = select_piece("b")

                        if piece != Empty and piece.color == "b":
                            # sprawdzenie dostępnych ruchów
                            player_moves = piece.gen_legal_moves(board)
                            # print(player_moves)
                            # podświetlenie dostępnych ruchów
                            board.highlight_optional_moves(player_moves)
                            selected = True

                    elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                        board.unhighlight_optional_moves()
                        square = select_square()

                        if square in player_moves:
                            oldx = piece.x
                            oldy = piece.y
                            dest = board.array[square[0]][square[1]]

                            # MCTS =============================================
                            # Przekazanie danych do drzewa
                            node = TreeNode(player='b', _from='(%d, %d)' % (piece.y, piece.x), _to='(%d, %d)' % (square[0], square[1])) # inicjalizacja węzła
                            temp = current_node.add_child(node) # dodanie węzła do obecnego (poprzedniego) węzła
                            # zmiana obecnego węzła
                            if temp is not None:
                                current_node = temp
                            else:
                                current_node = node
                            # ===================================================

                            # wykonanie ruchu
                            board.move_piece(piece, square[0], square[1])
                            if dest:
                                sprites = reload_sprites()
                                all_sprites_list.empty()
                                all_sprites_list.add(reload_sprites())

                            selected = False
                            player = 1

                        elif (piece.y, piece.x) == square:
                            piece.unhighlight()
                            selected = False
                        else:
                            pygame.display.update()
                            board.highlight_optional_moves(player_moves)
                            pygame.time.wait(1000)

                # pygame.display.update()
                # board.highlight_optional_moves(player_moves)
                # pygame.time.wait(1000)

        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)
        run_flag = 1

        arr = []
        for j in range(9):
            for piecee in board.array[j]:
                arr.append(piecee.color + piecee.symbol)

        # check end game
        if 'wN' not in arr:
            gameover = True
            winner = "Black"
        elif 'bN' not in arr:
            gameover = True
            winner = "White"

        current_move = arr[40]
        if previous_move == 'wN' and current_move == "_N":
            gameover = True
            winner = "White"
        elif previous_move == 'bN' and current_move == "_N":
            gameover = True
            winner = "Black"

    print("Wygrał: ", winner)
    current_node.update_score(winner[0].lower()) # Propagacja wsteczna od ostatniego węzła
    print_tree(game_tree) #wyświetlenie zaktualizowanego drzewa
