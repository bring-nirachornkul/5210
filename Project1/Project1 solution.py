import random
import math
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

    def __init__(self, a_ware_house: list, order: list, items=dict(), around=[0, 0, 0, 0], path=[], score=0):
        self.warehouse = a_ware_house
        self.order = order
        self.items = items
        self.around = around
        self.path = path
        self.score = score
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
        shelves_to_go = [''.join(list(shelf.keys())) for shelf in self.order]
        move = 0
        while shelves_to_go:  # Until the robot picked up all items in an order
            print(f'shelves_to_go: {shelves_to_go}')
            print(f'Move: {move}')
            print(f'Current position: {self.rpos, self.cpos}')
            peak_all_directions = [[self.rpos, self.peak_west()], [self.rpos, self.peak_east()],
                                   [self.peak_north(), self.cpos], [self.peak_south(), self.cpos]]
            peak_all_directions = [i for i in peak_all_directions if None not in i]
            print(f'peak_all_directions: {peak_all_directions}')
            # print(f'peak_all_directions: {peak_all_directions}')
            # Scan around to see how many surrounding shelves have the item in the order
            if self.peak_west() and self.warehouse[self.rpos, self.peak_west()] in shelves_to_go:
                print(f'around 0 : {self.warehouse[self.rpos, self.peak_west()]}')
                self.around[0] = 1
            if self.peak_east() and self.warehouse[self.rpos, self.peak_east()] in shelves_to_go:
                print(f'around 1 : {self.warehouse[self.rpos, self.peak_east()]}')
                self.around[1] = 1
            if self.peak_north() and self.warehouse[self.peak_north(), self.cpos] in shelves_to_go:
                print(f'around 2 : {self.warehouse[self.peak_north(), self.cpos]}')
                self.around[2] = 1
            if self.peak_south() and self.warehouse[self.peak_south(), self.cpos] in shelves_to_go:
                print(f'around 3 : {self.warehouse[self.peak_south(), self.cpos]}')
                self.around[3] = 1

            print(f'self.around: {self.around}')

            # Determine the direction to move
            if sum(self.around) == 0:
                self.rpos, self.cpos = random.choice(peak_all_directions)
                print(f'Current position after choice: {self.rpos, self.cpos}')
                self.score -= 1

            elif sum(self.around) == 1:
                # Find the index of the only grid square and move to that only grid square
                where_to_go[self.around.index(1)]()
                print(f'== 1 Current position after choice: {self.rpos, self.cpos}')
                self.score += 3

            elif sum(self.around) > 1:
                # make a random choice between the positions involved
                index_of_directions = [i for i, v in enumerate(self.around) if v == 1]
                where_to_go[random.choice(index_of_directions)]()
                print(f'> 1 Current position after choice: {self.rpos, self.cpos}')
                self.score += 3

            # Update the locations that the robot has followed so far
            self.path.append([self.rpos, self.cpos])

            # Determine what shelf it is
            name_of_shelf = self.warehouse[self.rpos, self.cpos]
            if name_of_shelf.isalpha() and name_of_shelf in shelves_to_go:
                print(f'name of shelf: {name_of_shelf}')
                print(f'order: {self.order}')
                # Pick up all items in the order that belong to a shelf
                for sub_order in self.order:
                    if name_of_shelf in sub_order:
                        print(f'sub_order[name_of_shelf]: {sub_order[name_of_shelf]}')
                        for code, quantity in sub_order[name_of_shelf].items():
                            self.get_items(code, quantity)
                        shelves_to_go.remove(name_of_shelf)
            # Reset around
            self.around = [0, 0, 0, 0]
            move += 1
            print(f'score: {self.score}')
            print()


'''
This is an example of the list of all orders
    Data structure: list of dict of dict
        The first dict:
        Data structure: Dict of dict
        key: name of the shelf
        value: a dictionary that represents all items that can be found in a shelf
            Data structure: Dict
            key: the code of the item in the shelf
            value: the amount of the items in the order
'''
order = [{'A': {'ISFS': 3, 'IJAY9A': 2}}, {'B': {'9FUSF': 1, '9KJC3': 2}}, {'C': {'89ADA': 1, 'F9S9': 9}}]

'''
This is an example of a map of a ware house 
    Data structure: 2D array
    Size: 6x6
    0 represents no shelf
    A capital letter represents the name of the shelf
'''
warehouse = np.array([[0, 0, 'D', 0, 0, 0], [0, 'A', 0, 0, 'G', 0], ['E', 0, 'B', 0, 'I', 0],
                     [0, 'C', 0, 0, 0, 0], [0, 0, 'F', 0, 0, 'H'], [0, 0, 0, 'J', 0, 0]])
avg_score = 0
shortest_path, longest_path = [], []
min_score = math.inf
max_score = -math.inf
episodes = 10
for episode in range(episodes):
    print(f'Episode {episode}')
    robot = Robot(warehouse, order)
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