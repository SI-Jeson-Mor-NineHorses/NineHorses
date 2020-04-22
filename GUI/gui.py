import pygame
import sys
from LOGIC.board import *
pygame.init()
pygame.font.init()

# Ustawienia okna gry
screen = pygame.display.set_mode((800, 60 * 9))
pygame.display.set_caption('Python Jeson Mor Game')
clock = pygame.time.Clock() #odświeżanie okna

# Załadowanie wygerowanej planszy
bg = pygame.image.load("assets/board.png").convert()
player = 1

board = Board()


global all_sprites_list, sprites
all_sprites_list = pygame.sprite.Group()
sprites = [piece for row in board.array for piece in row if piece]
all_sprites_list.add(sprites)

def select_piece(color):
    pos = pygame.mouse.get_pos()
    # get a list of all sprites that are under the mouse cursor
    # lista wszystkich duszków, ktore sa pod kursorem myszy
    clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]

    # podświetla i zwaraca jeśli jest to pionek gracza
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        clicked_sprites[0].highlight()
        return clicked_sprites[0]


def select_square():
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = y // 60
    return (y, x)

def run_game():

    gameover = False
    selected = False
    trans_table = dict()
    checkWhite = False
    player = 1

    previous_move = ''
    current_move = ''

    while not gameover:
        previous_move = current_move
        if player == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # wybór pionka do wykonania ruchu
                elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                    piece = select_piece("w")

                    # generuje "legalne" ruchy pionka
                    if piece != None:
                        player_moves = piece.gen_legal_moves(board)
                        selected = True

                # pionek wybrany -> wybór ruchu
                elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                    square = select_square()

                    # sprawdza czy wybrane pole jest w zasięgu dozwolonych ruchów
                    if square in player_moves:
                        oldx = piece.x
                        oldy = piece.y
                        dest = board.array[square[0]][square[1]]

                        # uaktualnienie sprites list
                        board.move_piece(piece, square[0], square[1])

                        if dest:  # usuwa "duszki", ktore zostaly zbite
                            all_sprites_list.remove(dest)
                            sprites.remove(dest)

                        selected = False
                        player = 2

                    # anuluje ruch, jezeli wybrane zostalo to samo pole
                    elif (piece.y, piece.x) == square:
                        piece.unhighlight()
                        selected = False

                    # ruch jest nieważny
                    else:
                        pygame.display.update()
                        pygame.time.wait(1000)
        # drugi gracz
        if player == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                    piece = select_piece("b")

                    if piece != None:
                        player_moves = piece.gen_legal_moves(board)
                        selected = True

                elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                    square = select_square()

                    if square in player_moves:
                        oldx = piece.x
                        oldy = piece.y
                        dest = board.array[square[0]][square[1]]

                        board.move_piece(piece, square[0], square[1])

                        if dest:
                            all_sprites_list.remove(dest)
                            sprites.remove(dest)

                        selected = False
                        player = 1

                    elif (piece.y, piece.x) == square:
                        piece.unhighlight()
                        selected = False

                    else:
                        pygame.display.update()
                        pygame.time.wait(1000)

        arr = []
        for j in range(9):
            for piecee in board.array[j]:
                if piecee != None:
                    arr.append(piecee.color + piecee.symbol)
                else:
                    arr.append("--")


        # check end game
        if 'wN' not in arr or 'bN' not in arr:
            gameover = True

        current_move = arr[40]
        if (previous_move == 'wN' or previous_move == 'bN') and current_move == "--":
            gameover = True


        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)

    print("KONIEC")
#        board.print_to_terminal()


if __name__ == "__main__":
    run_game()