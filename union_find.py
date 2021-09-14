cells = {}

class Node():
    def __init__(self, par = None, val = -1, rank = 0):
        self.par = par if par else self
        self.val = val
        self.rank = rank

def create(val):
    node = Node(val = val)
    cells[val] = node

def find(data):
    node = cells.get(data) if type(data) != Node else data
    if node.par != node:
        # path compression - set all nodes' parent to point to the leader of the set. 
        node.par = find(node.par)

    return node.par

def union(val1, val2):
    lead1 = find(val1)
    lead2 = find(val2)

    # leaders are different, both values are in different sets.
    if lead1 != lead2:
        if lead1.rank >= lead2.rank:
            if lead1.rank == lead2.rank:
                lead1.rank += 1
            
            lead2.par = lead1
        else:
            lead1.par = lead2

def sameSet(val1, val2):
    return find(val1) == find(val2)