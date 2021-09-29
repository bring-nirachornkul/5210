import random
from faker import Faker


class Order:
    '''
    This creates an order with random numbers representing
    divivion, items ordered, shelf
    Assumption: The quantity of each item is 1, and the number of shelves is equal to the number of items
    '''
    division = random.randint(1, 15)
    number_of_items = random.randint(1, 3)
    shelves = random.sample(range(1, 63), number_of_items)

    def __init__(self):
        self.divison = Order.division
        self.shelves = [{shelf: Faker().ean(length=13)} for shelf in Order.shelves]

    def __repr__(self):
        return f'Divison: {self.division}\nShelf & barcode: {self.shelves}'


class Node:
    def __init__(self, weight=0, number=1, parent=None):
        self.l = None
        self.r = None
        self.parent = parent
        self.weight = weight
        self.number = number

    def __repr__(self):
        return f'Node number {self.number} has weight of {self.weight}'


class Tree:
    count = 0
    weights = []

    @staticmethod
    def halves(n):
        '''
        This method returns the path from the root node to the current one
        '''
        r = []
        path = ''
        while n != 0:
            r.append(n)
            n //= 2
        return r[::-1]

    def __init__(self):
        self.root = Node()
        Tree.count += 1
        self.root.number = Tree.count
        Tree.weights.append(0)

    def getRoot(self):
        return self.root

    def add(self, weight):
        if self.root is None:
            self.root = Node()
            Tree.count += 1
            self.root.number = Tree.count
            Tree.weights.append(0)
        else:
            current = self.getRoot()
            next_node = current
            Tree.count += 1
            if Tree.count == 2:
                current.l = Node(weight, 2)
                next_node = current.l
                next_node.parent = current
            elif Tree.count == 3:
                current.r = Node(weight, 3)
                next_node = current.r
                next_node.parent = current
            else:
                paths = self.halves(Tree.count)[:-1]
                cur = paths[0]
                for path in paths[1:]:
                    if cur * 2 == path:
                        current = current.l
                    else:
                        current = current.r
                    cur = path
                if cur * 2 == Tree.count:
                    current.l = Node(weight, Tree.count)
                    next_node = current.l
                    next_node.parent = current
                else:
                    current.r = Node(weight, Tree.count)
                    next_node = current.r
                    next_node.parent = current
        Tree.weights.append(weight)

    def print_tree(self):
        '''
        This method prints a list of all nodes and their respective weights
        '''
        if Tree.count > 0:
            print([(count, weight) for count, weight in zip(range(1, Tree.count + 1), Tree.weights)])
        else:
            print('The tree needs to have some nodes')

    def Postorder(self, root):
        if root:
            self.Postorder(root.l)
            self.Postorder(root.r)
            print(root.number)


tree = Tree()
tree.add(20)
tree.add(20)
tree.add(20)
tree.add(30)
tree.add(40)
tree.add(10)
tree.add(10)
tree.add(20)
tree.add(30)
tree.add(20)
tree.add(30)
tree.add(20)
tree.add(20)
tree.add(20)

