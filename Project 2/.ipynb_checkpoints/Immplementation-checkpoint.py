import random
from math import log2
from typing import Union
from faker import Faker


# Question 3
class Order:
    '''Creates an order from random numbers

    Args:
        divivion: The high of random range of division
        items ordered: The high of random range of the quantity of items ordered
        shelf: The high of random range of the quantity of shelves
    Assumption:
        The quantity of each item is 1, and the number of shelves is equal to the number of items
    '''
    number_of_items = random.randint(1, 3)
    shelves = random.sample(range(1, 63), number_of_items)

    def __init__(self, division, shelves: Union[list, int]):
        self.division = division
        self.shelves = shelves

    def __repr__(self):
        return f'Divison: {self.division}\nShelves: {self.shelves}'


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

    def __init__(self, name: str):
        self.name = name
        self.root = Node()
        self.tail = self.root
        self.root.level = 1
        self.current_node = self.root

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
            current_node = self.getRoot()
            next_node = current_node
            if self.tail.number == 1:
                current_node.l = Node(cost)
                next_node = current_node.l
                next_node.parent = current_node
            elif self.tail.number == 2:
                current_node.r = Node(cost)
                next_node = current_node.r
                next_node.parent = current_node
            else:
                paths = self.halves(self.tail.number + 1)[:-1]
                # print(f'tail = {self.tail.number}, paths = {paths}')
                for path in paths[1:]:
                    if current_node.number * 2 == path:
                        current_node = current_node.l
                    else:
                        current_node = current_node.r
                # print(f'After for loop, current node = {current_node.number}')
                if current_node.number * 2 == self.tail.number + 1:
                    current_node.l = Node(cost, self.tail.number + 1)
                    next_node = current_node.l
                    next_node.parent = current_node
                    # print(f'Added {next_node.number} to the left of {current_node.number}')
                else:
                    current_node.r = Node(cost, self.tail.number + 1)
                    next_node = current_node.r
                    next_node.parent = current_node
                    # print(f'Added {next_node.number} to the right of {current_node.number}')
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

    def back_track(self):
        '''Returns a back track from the current node to the tree's root
            Args:
                 number: The node's id
            Returns:
                the back track path

        '''
        a_node = self.current_node
        self.current_node = self.getRoot()
        return self.halves(a_node.number)[::-1]

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

    # Question 4
    def ids(self, number):
        '''
        This method makes use of iterative deepening search for a specific node
        Assumption: The depth limit can be the tree's depth
        '''
        if number < self.root.number or number > self.tail.number:
            return f'The node number does not exist in the tree'
        visited = []
        while self.current_node and self.current_node.number != number:
            if self.current_node.number not in visited:
                visited.append(self.current_node.number)
            if self.current_node.l and self.current_node.l.number not in visited:
                self.current_node = self.current_node.l
            elif self.current_node.r and self.current_node.r.number not in visited:
                self.current_node = self.current_node.r
            else:
                self.current_node = self.current_node.parent
        # print(f'Current node after while loop: {self.current_node.number}')
        if not self.current_node or self.current_node.number != number:
            return f'The node number {number} could not be found'
        else:
            visited.append(self.current_node.number)
        return visited

    def go_to_division(self, order: Order):
        return self.ids(order.division)

    def go_to_shelves(self, order: Order):
        if isinstance(order.shelves, list):
            paths = [self.ids(shelf) for shelf in order.shelves]
        else:
            paths = self.ids(order.shelves)
        return paths


costs = [20, 20, 20, 30, 40, 10, 10, 20, 30, 20, 30, 20, 20, 20]
tree = Tree('divisions')
for cost in costs:
    tree.add(cost)

sub_tree = Tree('shelves')
for i in range(1, 63):
    sub_tree.add(1)
# sub_tree.print_tree()

# Question 5
# trial_order = Order(division=6, shelves=33)
# print(f'Trial oder: division = {trial_order.division}, shelf = {trial_order.shelves}')
# division_path = tree.go_to_division(trial_order)
# shelf_path = sub_tree.go_to_shelves(trial_order)
# print(f'Path to division: {division_path}, length = {len(division_path)}')
# print(f'Path to shelf: {shelf_path}, length = {len(shelf_path)}')
# tree.current_node = tree.getRoot()
# sub_tree.current_node = sub_tree.getRoot()

# Question 6
def return_shortest_path(a, b):
    '''Returns the shortest path between a and b

        Args:
            a, b: paths to be compared
    '''
    # Check if b is a 1d list
    if all(isinstance(i, int) for i in b):
        return b if len(a) > len(b) else a
    for sub_list in b:
        a = sub_list if len(a) > len(sub_list) else a
    return a

def return_longest_path(a, b):
    '''Returns the longest path between a and b

        Args:
            a, b: paths to be compared
    '''
    # Check if b is a 1d list
    if all(isinstance(i, int) for i in b):
        return a if len(a) > len(b) else b
    for sub_list in b:
        a = a if len(a) > len(sub_list) else sub_list
    return a

total_orders = 100
orders = [Order(division=random.randint(1, tree.tail.number),
                shelves=random.sample(range(1, tree.tail.number), random.randint(1, 3))) for _ in range(total_orders)]
total_path_length = 0
division_shortest_path, division_longest_path = [], []
shelf_shortest_path, shelf_longest_path = [], []
for index, order in enumerate(orders, 1):
    # print(f'Order {index}')
    # print(order)
    # print(f'The path from division {tree.current_node.number} to division {order.division} :', end=' ')
    division_path = tree.go_to_division(order)
    shelf_paths = sub_tree.go_to_shelves(order)
    division_shortest_path = return_shortest_path(division_shortest_path, division_path)
    division_longest_path = return_longest_path(division_longest_path, division_path)
    shelf_shortest_path = return_shortest_path(shelf_shortest_path, shelf_paths)
    shelf_longest_path = return_longest_path(shelf_longest_path, shelf_paths)

    # print(f'{division_path}, length = {len(division_path)}')
    total_path_length += len(division_path)
    for shelf_path in shelf_paths:
        # print(
        #     f'The path from shelf {shelf_path[0]} to shelf {shelf_path[-1]} : {shelf_path}, length = {len(shelf_path)}')
        total_path_length += len(shelf_path)
    back_track = sub_tree.back_track()
    # print(
    #     f'The back track path from shelf {sub_tree.current_node.number} to the entrance of division {order.division}: {back_track}, length = {len(back_track)}')
    # print()
avg_path_length = total_path_length / total_orders
print(f'Average path length in {total_orders} orders: {avg_path_length}')
print(f'The shortest division path of length {len(division_shortest_path)}: {division_shortest_path}')
print(f'The longest division path of length {len(division_longest_path)}: {division_longest_path}')
print(f'The shortest shelf path of length {len(shelf_shortest_path)}: {shelf_shortest_path}')
print(f'The longest shelf path of length {len(shelf_longest_path)}: {shelf_longest_path}')