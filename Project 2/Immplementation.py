import random
from faker import Faker


def create_order():
    '''
    This creates an order with random numbers representing
    divivion, items ordered, shelf
    Assumption: The quantity of each item is 1, and the number of shelves is equal to the number of items
    '''
    fake_data = Faker()
    division = random.randint(1, 15)
    number_of_items = random.randint(1, 3)
    shelves = random.sample(range(1, 63), number_of_items)
    return (division, [{shelf: fake_data.ean(length=13)} for shelf in shelves])

print(create_order())