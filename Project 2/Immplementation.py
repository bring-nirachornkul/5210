import random
from math import log2
from faker import Faker


class Order:
    '''Creates an order from random numbers

    Args:
        divivion: The high of random range of division
        items ordered: The high of random range of the quantity of items ordered
        shelf: The high of random range of the quantity of shelves
    Assumption:
        The quantity of each item is 1, and the number of shelves is equal to the number of items
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
    def __init__(self, cost=0, number=1):
        self.l = None
        self.r = None
        self.parent = None
        self.level = None
        self.cost = cost
        self.number = number

    def __repr__(self):
        return f'Node number {self.number} has the cost of {self.cost}'


class Tree:

    @staticmethod
    def halves(n):
        '''Creates the path from the root node to the current one

            Args:
                n: The destination node's id
            Returns:
                the path from the root node to the current one
        '''
        r = []
        path = ''
        while n != 0:
            r.append(n)
            n //= 2
        return r[::-1]

    @staticmethod
    def find_level(number):
        '''Applies the binary log to find the level of a node in the tree

            Args:
                number: The node's id
            Returns:
                The level of the node in the tree
        '''
        return int(log2(number + 1))

    def __init__(self, name):
        self.name = name
        self.root = Node()
        self.tail = self.root
        self.root.level = 1

    def getRoot(self):
        return self.root

    def add(self, cost):
        '''Inserts the new node to its appropriate position in accordance with the tree structure

            Args:
                cost: The node's path cost from its parent
        '''

        if self.root is None:
            self.root = Node()
            self.tail = self.root
        else:
            current = self.getRoot()
            next_node = current
            if self.tail.number == 1:
                current.l = Node(cost)
                next_node = current.l
                next_node.parent = current
            elif self.tail.number == 2:
                current.r = Node(cost)
                next_node = current.r
                next_node.parent = current
            else:
                paths = self.halves(self.tail.number + 1)[:-1]
                cur = paths[0]
                for path in paths[1:]:
                    if cur * 2 == path:
                        current = current.l
                    else:
                        current = current.r
                    cur = path
                if cur * 2 == self.tail.number:
                    current.l = Node(cost, self.tail.number)
                    next_node = current.l
                    next_node.parent = current
                else:
                    current.r = Node(cost, self.tail.number)
                    next_node = current.r
                    next_node.parent = current
            next_node.level = self.find_level(self.tail.number)
            next_node.number = self.tail.number + 1
            self.tail = next_node


    def find_node(self, number):
        '''Returns a path from root to the node which has the number

            Args:
                 number: The node's id
        '''
        if 0 < number <= Tree.count:
            paths = self.halves(number)[1:]
            path_from_root = ['R' if p % 2 else 'L' for p in paths]
            return path_from_root
        return 'The node number does not exist in the tree'

    def back_track(self, number):
        '''Returns a back track from a specific node to the tree's root

            Args:
                 number: The node's id
        '''

        if 0 < number <= Tree.count:
            return self.halves(number)[::-1][1:]
        return 'The node number does not exist in the tree'

    def print_tree(self):
        '''Prints a list of all nodes and their respective costs
        '''
        if self.tail.number > 0:
            print(f'The tree of {self.name}:')
            for i in range(1, self.tail.number + 1):
                level = int(log2(i)) + 1
                print(f'Level {level}', end='')
                print(f'Node {i}'.center(20))
                if int(log2(i + 1)) + 1 > level:
                    print()
        else:
            print('The tree needs to have some nodes')

    def Postorder(self, root):
        '''Prints the tree in post order

            Args:
                root: The tree's starting point
        '''
        if root:
            self.Postorder(root.l)
            self.Postorder(root.r)
            print(f'Current node number: {root.number}, level: {root.level}')
            if root.parent:
                print(f'parent is {root.parent.number}')
            print()

    def ids(self, number, depth_limit=None):
        '''
        This method makes use of iterative deepening search for a specific node
        '''
        if number < 1 or number > Tree.count:
            return f'The node number does not exist in the tree'
        if depth_limit == None:
            depth_limit = Tree.depth
        visited = []
        current_node = self.getRoot()
        while current_node and current_node.level <= depth_limit - 1 and current_node.number != number:
            print(
                f'Current node number: {current_node.number},  level: {current_node.level}, depth limit: {depth_limit}')
            if current_node.number not in visited:
                visited.append(current_node.number)
            if current_node.l and current_node.l.number not in visited:
                current_node = current_node.l
            elif current_node.r and current_node.r.number not in visited:
                current_node = current_node.r
            else:
                current_node = current_node.parent
        print(f'Current node after while loop: {current_node.number}')
        if not current_node or current_node.number != number:
            return f'The node number {number} could not be found'
        else:
            visited.append(current_node.number)
        return visited


costs = [20, 20, 20, 30, 40, 10, 10, 20, 30, 20, 30, 20, 20, 20]
divisons = Tree('divisions')
for cost in costs:
    divisons.add(cost)
# divisons.print_tree()

shelves = Tree('shelves')
for i in range(63):
    shelves.add(1)
# shelves.print_tree()

# tree.ids(15)
# print(tree.back_track(12))
# print(tree.find_node(12))
# root = tree.getRoot()
# tree.Postorder(root)
