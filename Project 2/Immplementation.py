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


order = Order()
print(order)
