import random
from collections import Counter

'''
orders is a list representing all orders
every nested list represents an order
    key: all items that can be found in a shelf
    value: a dictionary having:
        key: the code of the item in the shelf
        value: the amount of the items in the order
'''
orders = [[{'A': {'ISFS': 3, 'IJAY9A': 2}}, {'B': {'9FUSF': 1, '9KJC3': 2}}],
          [{'B': {'9SDF': 3, 'KA9D': 9}}, {'C': {'89ADA': 1, 'F9S9': 9}}]]

warehouse = [[0, 0, 'D', 0, 0, 0], [0, 'A', 0, 0, 'G', 0], ['E', 0, 'B', 0, 'I', 0],
             [0, 'C', 0, 0, 0, 0], [0, 0, 'F', 0, 0, 'H'], [0, 0, 0, 'J', 0, 0]]


class Robot:

    # Initialize a robot with the ware house map, a list of all orders,
    #   a record of the all squares that the robot has moved in,
    #   the items of an order that the robot has picked
    #   and all grids around the robot: w, e, n, s
    def __init__(self, a_ware_house: list, an_orders=None, items=dict(), around=[0, 0, 0, 0]):
        self.warehouse = a_ware_house
        self.orders = an_orders
        self.position = [0, 0]
        self.not_passed = [[row, col] for row in range(len(self.warehouse)) for col in range(len(self.warehouse[0]))]
        self.items = items
        self.around = around

    def go_west(self):
        if self.position[1] > 0:
            self.position[1] -= 1

    def go_east(self):
        if self.position[1] < len(self.warehouse[0]) - 1:
            self.position[1] += 1

    def go_north(self):
        if self.position[0] > 0:
            self.position[0] -= 1

    def go_south(self):
        if self.position[0] < len(self.warehouse) - 1:
            self.position[0] += 1

    def peak_west(self):
        if self.position[1] > 0:
            return self.position[0], self.position[1] - 1

    def peak_east(self):
        if self.position[1] < len(self.warehouse[0]) - 1:
            return self.position[0], self.position[1] + 1

    def peak_north(self):
        if self.position[0] > 0:
            return self.position[0] - 1, self.position[1]

    def peak_south(self):
        if self.position[0] < len(self.warehouse) - 1:
            return self.position[0] + 1, self.position[1]

    def get_items(self, item, quantity):
        # Robot picks all items in a shelf that is included in an order
        self.items[item] += quantity

    def take_order(self):
        look_up = {
            0: self.go_west(),
            1: self.go_east(),
            2: self.go_north(),
            3: self.go_south(),
        }
        peak_all_directions = [self.peak_west(), self.peak_east(), self.peak_north(), self.peak_south()]
        self.not_passed.remove(self.position)
        for order in self.orders:
            shelves_to_go = [''.join(list(shelf.keys())) for shelf in order]

            # Look around to see how many surrounding shelves have the item in the order
            if self.peak_west() and self.warehouse[self.peak_west()[0]][self.peak_west()[1]] in shelves_to_go:
                self.around[0] = 1
            if self.peak_east() and self.warehouse[self.peak_east()[0]][self.peak_east()[1]] in shelves_to_go:
                self.around[1] = 1
            if self.peak_north() and self.warehouse[self.peak_north()[0]][self.peak_north()[1]] in shelves_to_go:
                self.around[2] = 1
            if self.peak_south() and self.warehouse[self.peak_south()[0]][self.peak_south()[1]] in shelves_to_go:
                self.around[3] = 1

            # Determine the direction to move
            if sum(self.around) == 0:
                next_location = random.choice(peak_all_directions)
                while self.warehouse[next_location[0]][next_location[1]] not in self.not_passed:
                    next_location = random.choice(peak_all_directions)
                self.position = [next_location]

            elif sum(self.around) == 1:
                # Find the index of the only grid square and move to that only grid square
                look_up[self.around.index(1)]

            elif sum(self.around) > 1:
                # make a random choice between the positions involved
                index_of_directions = [i for i, v in enumerate(self.around) if v == 1]
                look_up[random.choice(index_of_directions)]

            # Update robot's location
            self.not_passed.remove(self.position)


            # [{'A': {'ISFS': 3, 'IJAY9A': 2}}, {'B': {'9FUSF': 1, '9KJC3': 2}}]