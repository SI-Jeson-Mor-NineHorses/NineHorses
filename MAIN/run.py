from MAIN.GUI.gui import run_game, load_tree, save_tree

if __name__ == "__main__":
    '''
    NineHorses PvP Game
    '''
    tree = load_tree(file_name="game_moves.json")  # wczytanie drzewa z pliku (nazwa pliku przekazana jako parametr)
    run_game(tree,0) # rozpoczęcie rozgrywki (drzewo rozgrywki, tryb gry)
    save_tree(tree, file_name="game_moves.json") # zapisanie drzewa do pliku (nazwa pliku przekazana jako parametr)
