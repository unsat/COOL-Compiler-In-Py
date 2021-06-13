from copy import deepcopy, copy

def read_lst(func, fin, args=[]):
    count = int(fin.readline())
    lst = []
    for i in range(count):
        lst.append(func(fin, *args))
    return lst

class Pedigree():
    class Node():
        def __init__(self, name):
            self.name = name
            self.parent = None
            self.children = []
        def __str__(self):
            return self.name
        def __repr__(self):
            return self.__str__()
        def set_parent(self, p):
            self.parent = p
        def get_children(self):
            return self.children
        def add_child(self, c):
            self.children.append(c)
        def rm_child(self, c):
            self.children = [n for n in self.children if n is not c]
        def path_to_root(self):
            if self.parent == None:
                return [self.name]
            else:
                return self.parent.path_to_root() + [self.name]
    def __init__(self):
        self.nodes = {}

    def get_node(self, name):
        if not name in self.nodes:
            self.nodes[name] =  Pedigree.Node(name)
        return self.nodes[name]

    def has_node(self, name):
        return name in self.nodes

    def add_node(self, name):
        self.get_node(name)

    def add_edge(self, p, c):
        parent = self.get_node(p)
        child  = self.get_node(c)
        parent.add_child(child)
        child.set_parent(parent)

    def is_child(self, a, b):
        return b in self.get_node(a).path_to_root()

    def lub(self, a, b):
        a = self.nodes[a].path_to_root()
        b = self.nodes[b].path_to_root()
        return [i for i,j in zip(a,b) if i==j][-1]

    def get_cycle(self):
        nodes = deepcopy(list(self.nodes.values()))
        for i in range(len(nodes)):
            for n in nodes:
                if not n.get_children():
                    if n.parent:
                        n.parent.rm_child(n)
                        n.set_parent(None)
        nodes = [n for n in nodes if n.get_children()]

        cycle = []
        if nodes:
            cycle = [nodes[0]]
            while True:
                next = cycle[-1].get_children()[0]
                if next in cycle:
                    cycle = cycle[cycle.index(next):]
                    break
                else:
                    cycle.append(next)
        return cycle


if __name__ == '__main__':
    pedi = Pedigree()
    pedi.add_edge("a","b")
    pedi.add_edge("b","c")
    pedi.add_edge("c","d")
    pedi.add_edge("c","z")
    pedi.add_edge("b","i")
    print(pedi.is_child("a","a"))
