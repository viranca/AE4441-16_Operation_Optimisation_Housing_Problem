
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random

# Libs
import numpy as np
from faker import Faker

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '08/11/2020'

################################################################################################################


class House_data:
    def __init__(self, nb_houses):
        # ----- Initialising tools

        # --> Seeding generators
        random.seed(345)

        # --> Initialising records
        self.nb_houses = nb_houses
        self.data = []

        self.gen_data()

    def gen_data(self):
        # ----- Initialising tools
        fake = Faker()

        # --> Creating houses
        for _ in range(self.nb_houses):
            self.data.append({"address": fake.address(),
                              "room_count": random.randint(1, 5),
                              "rent_per_room": random.randint(250, 650),
                              "location": {"x": random.randint(0, 100),
                                           "y": random.randint(0, 100)}
                              })

    def list_property(self, property):
        property_lst = []

        for i in range(len(self.data)):
            property_lst.append(self.data[i][property])

    def sort_by_property(self, property):
        # --> Sorting using insertion sort (smallest to largest)

        for j in range(1, len(self.data)):
            for i in range(j, 0, -1):
                if self.data[i][property] < self.data[i - 1][property]:
                    self.data[i][property], self.data[i - 1][property] = \
                        self.data[i - 1][property], self.data[i][property]


if __name__ == '__main__':
    houses = House_data(10)
    print(houses.data)