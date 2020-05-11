
class TreeNode(object):
    #  Generic tree node.
    # parent, play, state, unexpandedPlays
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    def add_child(self, node):
        assert isinstance(node, TreeNode)
        self.children.append(node)


def print_tree(node, file=None, _prefix="", _last=True):
    # print implementation from https://vallentin.dev/2016/11/29/pretty-print-tree
    print(_prefix, "`- " if _last else "|- ", node.name, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        print_tree(child, file, _prefix, _last)


def find_node(node, target_name):
    for i, child in enumerate(node.children):
        node = find_node(child, target_name)
        if node.name == target_name:
            return node
    return node


if __name__ == "__main__":
    t = TreeNode('*', [TreeNode('1', [TreeNode('1.1'), TreeNode('1.2')]), TreeNode('2'), TreeNode('3', [TreeNode('3.1'), TreeNode('3.2')])])
    print_tree(t)
    n_2 = find_node(t,  "_")
    n_2.add_child(TreeNode('NEW'))
    print_tree(t)


