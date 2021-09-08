import random
import math
from faker import Faker
import numpy as np


class Robot:
    """
    A class to represent a person.
    ...
    Attributes
    ----------
        warehouse: 2d array
            the ware house map
        order: list
            leftover items in the orders
        items: dict
            items that the robot has collected so far
        path: list
            the path the robot has followed,
        score: int
            if the robot goes to a grid square that does not have the ordered item: -1 else + 3
        around: list
            an array of length 4 representing the shelf that has the ordered item in corresponding
            to direction next to the robot in the pattern west / east / north / south
    """

    def __init__(self, a_ware_house: list, an_order: list):
        self.warehouse = a_ware_house
        self.order = an_order
        self.items = dict()
        self.around = [0, 0, 0, 0]
        self.path = []
        self.score = 0
        self.rpos = 0
        self.cpos = 0

    def go_west(self):
        if self.cpos > 0:
            self.cpos -= 1

    def go_east(self):
        if self.cpos < len(self.warehouse[0]) - 1:
            self.cpos += 1

    def go_north(self):
        if self.rpos > 0:
            self.rpos -= 1

    def go_south(self):
        if self.rpos < len(self.warehouse) - 1:
            self.rpos += 1

    def peak_west(self):
        if self.cpos > 0:
            return self.cpos - 1

    def peak_east(self):
        if self.cpos < len(self.warehouse[0]) - 1:
            return self.cpos + 1

    def peak_north(self):
        if self.rpos > 0:
            return self.rpos - 1

    def peak_south(self):
        if self.rpos < len(self.warehouse) - 1:
            return self.rpos + 1

    def get_items(self, item, quantity):
        # Robot picks all items in a shelf that is included in an order
        self.items[item] = quantity

    def proceed_order(self):
        where_to_go = {
            0: self.go_west,
            1: self.go_east,
            2: self.go_north,
            3: self.go_south,
        }
        self.rpos = self.cpos = 0
        self.path.append([self.rpos, self.cpos])
        shelves_to_go = sorted(sorted(i[0] for i in self.order))
        move = 0
        while shelves_to_go:  # Until the robot picked up all items in an order
            # print(f'shelves_to_go: {shelves_to_go}')
            # print(f'Move: {move}')
            # print(f'Current position: {self.rpos, self.cpos}')
            peak_all_directions = [[self.rpos, self.peak_west()], [self.rpos, self.peak_east()],
                                   [self.peak_north(), self.cpos], [self.peak_south(), self.cpos]]
            peak_all_directions = [i for i in peak_all_directions if None not in i]
            # print(f'peak_all_directions: {peak_all_directions}')

            # Scan around to see how many surrounding shelves have the item in the order
            if self.peak_west() and self.warehouse[self.rpos, self.peak_west()] in shelves_to_go:
                # print(f'around 0 : {self.warehouse[self.rpos, self.peak_west()]}')
                self.around[0] = 1
            if self.peak_east() and self.warehouse[self.rpos, self.peak_east()] in shelves_to_go:
                # print(f'around 1 : {self.warehouse[self.rpos, self.peak_east()]}')
                self.around[1] = 1
            if self.peak_north() and self.warehouse[self.peak_north(), self.cpos] in shelves_to_go:
                # print(f'around 2 : {self.warehouse[self.peak_north(), self.cpos]}')
                self.around[2] = 1
            if self.peak_south() and self.warehouse[self.peak_south(), self.cpos] in shelves_to_go:
                # print(f'around 3 : {self.warehouse[self.peak_south(), self.cpos]}')
                self.around[3] = 1

            # print(f'self.around: {self.around}')

            # Determine the direction to move
            if sum(self.around) == 0:
                self.rpos, self.cpos = random.choice(peak_all_directions)
                # print(f'Current position after choice: {self.rpos, self.cpos}')
                self.score -= 1

            elif sum(self.around) == 1:
                # Find the index of the only grid square and move to that only grid square
                where_to_go[self.around.index(1)]()
                # print(f'== 1 Current position after choice: {self.rpos, self.cpos}')
                self.score += 3

            elif sum(self.around) > 1:
                # make a random choice between the positions involved
                index_of_directions = [i for i, v in enumerate(self.around) if v == 1]
                where_to_go[random.choice(index_of_directions)]()
                # print(f'> 1 Current position after choice: {self.rpos, self.cpos}')
                self.score += 3

            # Update the locations that the robot has followed so far
            self.path.append([self.rpos, self.cpos])

            # Determine what shelf it is
            name_of_shelf = self.warehouse[self.rpos, self.cpos]
            if name_of_shelf.isalpha() and name_of_shelf in shelves_to_go:
                # print(f'name of shelf: {name_of_shelf}')
                # print(f'order: {self.order}')
                # Pick up all items in the order that belong to a shelf
                for shelf, details in self.order:
                    if shelf == name_of_shelf:
                        # print(f'sub_order[name_of_shelf]: {sub_order[name_of_shelf]}')
                        for code, quantity in details:
                            self.get_items(code, quantity)
                        shelves_to_go.remove(name_of_shelf)
            # Reset around
            self.around = [0, 0, 0, 0]
            move += 1
            # print(f'score: {self.score}')
            # print()


def create_fake_order(warehouse_map, number_of_shelf: int, number_of_items_in_a_shelf: int, random_quantity=5):
    """
    This function creates a fake order with
        Data structure: list
            The first layer
            Data structure: tuple
                Shelf: The name of the shelf
                Details: It contains all items that can be found in the specific shelf
                    Data structure: list of tuples
                    Each tuple has:
                        Code of the item
                        Quantity of the item as a random number from 1 to random_quantity
    """

    faker = Faker()

    # Extract all shelves from the warehouse map
    all_shelves = ''.join(element for row in warehouse_map for element in row if element.isalpha())

    # Create a list of random number_of_shelf shelves out of all_shelves lexicographically
    order_shelves = sorted(random.sample(all_shelves, number_of_shelf))

    my_order = []
    for shelf in order_shelves:
        my_order.append(
            (shelf,
             [(faker.ean(length=13), random.randint(1, random_quantity)) for _ in range(number_of_items_in_a_shelf)]))
    return my_order


def try_warehouses(warehouse, episodes=1000):
    avg_score = 0
    shortest_path, longest_path = [], []
    min_score = math.inf
    max_score = -math.inf
    for episode in range(episodes):
        # print(f'Episode {episode}')
        robot = Robot(warehouse,
                      create_fake_order(warehouse_map=warehouse, number_of_shelf=2, number_of_items_in_a_shelf=3))
        robot.proceed_order()
        if min_score > robot.score:
            min_score = robot.score
            shortest_path = robot.path[:]
        if max_score < robot.score:
            max_score = robot.score
            longest_path = robot.path[:]
        avg_score += robot.score
    avg_score /= episodes
    print(f'Average score after {episodes} episodes is {avg_score}')
    print(f'Min score is : {min_score}')
    print(f'Max score is : {max_score}')
    print(f'The shortest path is {shortest_path} with {min_score} points')
    print(f'The longest path is {longest_path} with {max_score} points')


'''
This is an example of a map of a ware house 
    Data structure: 2D array
    Size: 6x6
    0 represents no shelf
    A capital letter represents the name of the shelf
'''

warehouse1 = np.array([[0, 0, 'D', 0, 0, 0], [0, 'A', 0, 0, 'G', 0], ['E', 0, 'B', 0, 'I', 0],
                       [0, 'C', 0, 0, 0, 0], [0, 0, 'F', 0, 0, 'H'], [0, 0, 0, 'J', 0, 0]])
warehouse2 = np.array([[0, 0, 'A', 0, 'P', 0], ['D', 0, 'B', 0, 'M', 0], ['E', 0, 'F', 0, 'K', 0],
                       ['C', 0, 'H', 0, 0, 'O'], ['G', 0, 'J', 0, 0, 'Q'], ['I', 0, 0, 0, 'N', 0]])
try_warehouses(warehouse1, 10)
# try_warehouses(warehouse2)
