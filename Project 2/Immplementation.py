import random
import math
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
    def __init__(self, weight=0, number=1):
        self.l = None
        self.r = None
        self.parent = None
        self.weight = weight
        self.number = number

    def __repr__(self):
        return f'Node number {self.number} has weight of {self.weight}'


class Tree:
    count = 0
    weights = []
    height = 1

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
        '''
        This method automatic insert the new node to its appropriate position in accordance with the tree structure
        '''
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
        Tree.height = int(math.log2(Tree.count + 1))

    def find_node(self, number):
        '''
        This method returns a path from root to the node which has the number
        '''
        if 0 < number <= Tree.count:
            paths = self.halves(number)[1:]
            path_from_root = ['R' if p % 2 else 'L' for p in paths]
            return path_from_root
        return 'The node number does not exist in the tree'

    def back_track(self, number):
        '''
        This method returns a back track from a specific node to the tree's root
        '''
        if 0 < number <= Tree.count:
            return self.halves(number)[::-1][1:]
        return 'The node number does not exist in the tree'

    def print_tree(self):
        '''
        This method prints a list of all nodes and their respective weights
        '''
        if Tree.count > 0:
            print([(count, weight) for count, weight in zip(range(1, Tree.count + 1), Tree.weights)])
        else:
            print('The tree needs to have some nodes')

    def Postorder(self, root):
        '''
        This method prints the tree in post order
        '''
        if root:
            self.Postorder(root.l)
            self.Postorder(root.r)
            print(f'Current node number: {root.number}')
            if root.parent:
                print(f'parent is {root.parent.number}')
            print()

    def ids(self, number, depth_limit=None):
        '''
        This method makes use of iterative deepening search for a specific node
        '''
        if depth_limit == None:
            depth_limit = Tree.height
        visited = []
        current_node = self.getRoot()
        while current_node and int(math.log2(current_node.number + 1)) <= Tree.height and current_node.number != number:
            if current_node.number not in visited:
                visited.append(current_node.number)
            if current_node.l and current_node.l.number not in visited:
                current_node = current_node.l
            elif current_node.r and current_node.r.number not in visited:
                current_node = current_node.r
            else:
                current_node = current_node.parent
        return visited


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
# tree.ids(15)
# print(tree.back_track(12))
# print(tree.find_node(12))
# root = tree.getRoot()
# tree.Postorder(root)
