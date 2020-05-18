import json
import math


class TreeNode(object):
    #  Generic tree node.
    def __init__(self, player='x', children=None, _from='', _to='', name='node', score=0, n_plays=0, n_wins=0,
                 parent=None):
        if name == 'node':
            self.name = "%s:%s=>%s" % (player, _from, _to)
        else:
            self.name = name  # nazwa przyjazna (do debugowania)
        self.player = player  # identyfikator gracza (w - biały, b - czarny)
        self.move_from = _from  # pole źródłowe
        self.move_to = _to  # pole docelowe

        self.n_plays = n_plays  # ile razy ruch został wykonany
        self.n_wins = n_wins  # ile razy ruch przyczynił się do wygranej

        self.parent = parent # rodzic węzła

        self.score = self.calc_UCB1(2) # współczynnik określający wartość węzła / miara wartości zagrania

        self.children = []  # tablica na potomków
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    # użycie algorytmu UCB1
    def calc_UCB1(self, bias):
        if self.n_plays == 0:
            return 0
        if self.parent is not None:
            parent_plays = self.parent.n_plays
        else:
            parent_plays = 1
        try:
            return (self.n_wins / self.n_plays) + math.sqrt(bias * math.log(parent_plays) / self.n_plays) # miara wartości zagrania
        except:
            # print("exception")
            return 0  # miara wartości zagrania

    # dodawanie węzłów do drzewa
    def add_child(self, node):
        exist = 0
        output = None
        if isinstance(node, TreeNode):
            for child in self.children:
                if child.name == node.name:
                    exist = 1
                    # child.n_plays += 1
                    output = child
            if not exist:
                # node.n_plays = 0
                node.parent = self
                self.children.append(node)
        return output

    # propagacja wsteczna
    def update_score(self, winner):
        if self.parent is not None:
            self.n_plays += 1
            if self.parent.player == winner:
                self.parent.n_wins += 1
            self.parent.update_score(winner)
            self.score = self.calc_UCB1(2)

    # def find_node(self, node=None, target=""):
    #     if node is None:
    #         print(self.name)
    #         node = self
    #         output = None
    #         for i, child in enumerate(self.children):
    #             node = child.find_node(node=child, target=target)
    #             if isinstance(node, TreeNode):
    #                 if node.name == target:
    #                     output = node
    #         return output
    #     else:
    #         for i, child in enumerate(node.children):
    #             if child.name == target:
    #                 return child
    #             else:
    #                 node = child.find_node(node=child, target=target)
    #                 if isinstance(node, TreeNode):
    #                     if node.name == target:
    #                         return node
    #     return node

    # serializacja drzewa
    def to_dict(self, node):
        return {'player': node.player, 'from': node.move_from, 'to': node.move_to, 'score': node.score,
                'n_plays': node.n_plays, 'n_wins': node.n_wins, 'name': node.name,
                'children': [self.to_dict(child) for child in node.children]}


# Zapisanie drzewa do pliku
def save_tree(node, file_name="dict.json"):
    json_data = json.dumps(node.to_dict(node))
    f = open(file_name, "w")
    f.write(json_data)
    f.close()


# Wczytanie zapisanego drzewa
def load_tree(file_name="dict.json"):
    def make_tree(temp_data):
        return TreeNode(player=temp_data['player'],
                        _from=temp_data['from'],
                        _to=temp_data['to'],
                        score=temp_data['score'],
                        n_plays=temp_data['n_plays'],
                        n_wins=temp_data['n_wins'],
                        name=temp_data['name'],
                        children=[make_tree(child) for child in temp_data['children']])

    try:
        json_file = open(file_name)
        with json_file:
            data = json.load(json_file)
            return make_tree(data)
    except IOError:
        save_tree(TreeNode(name='ROOT', n_plays=1, n_wins=1, children=[]), file_name)  # zapis pustego drzewa
        return load_tree(file_name)

# wyświetlenie drzewa w konsoli
def print_tree(node, file=None, _prefix="", _last=True):
    # print implementation from https://vallentin.dev/2016/11/29/pretty-print-tree
    if node.name == 'ROOT':
        print(_prefix, "`- " if _last else "|- ", node.name, sep="", file=file)
    else:
        print(_prefix, "`- " if _last else "|- ", node.score, "=", node.n_wins, "/", node.n_plays, sep="", file=file)
        # print(_prefix, "`- " if _last else "|- ", node.name, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        print_tree(child, file, _prefix, _last)


if __name__ == "__main__":
    t = TreeNode(name='ROOT', children=[])
    t.add_child(TreeNode(player='w', _from='(8, 1)', _to='(6, 4)')) # dodanie nowego węzła do węzła 't' (korzeń drzewa)
    print_tree(t) # wyświetlenie drzewa
    save_tree(t) # zapisanie drzewa do pliku (nazwa pliku domyślna)
    load_tree() # wczytanie drzewa z pliku (nazwa pliku domyślna)
    print_tree(t) # wyświetlenie drzewa
