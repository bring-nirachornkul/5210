orders = [{'A1': 1, 'A2': 4, 'B3': 6}, {'C2': 6, 'D8': 5}]
warehouse = [[0, 0, 'D', 0, 0, 0], [0, 'A', 0, 0, 'G', 0], ['E', 0, 'B', 0, 'I', 0], [0, 'C', 0, 0, 0, 0], [0, 0, 'F', 0, 0, 'H'], [0, 0, 0, 'J', 0, 0]]

class Robot:
    def __init__(self,a_ware_house, an_orders=None):
        self.warehouse = a_ware_house
        self.orders = an_orders
        self.position = [0, 0]

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