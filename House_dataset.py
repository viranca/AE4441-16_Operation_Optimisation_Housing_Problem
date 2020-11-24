
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
from math import sqrt

# Libs
import numpy as np
from faker import Faker

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '08/11/2020'

################################################################################################################


class House_dataset:
    def __init__(self,
                 nb_houses,
                 faculty_lst=["ae", "cs", "3me"]):
        # ----- Initialising tools
        # --> Seeding generators
        random.seed(345)

        # --> Initialising records
        self.nb_houses = nb_houses
        self.faculty_lst = faculty_lst

        self.data = []
        self.faculty_data = []

        self.gen_data()

    def gen_data(self):
        # ----- Initialising tools
        fake = Faker()

        # ----- Creating houses
        for i in range(self.nb_houses):
            self.data.append({"ref": str(i),        # ref is made a string to better work with dictionary format adopted
                              "address": fake.address(),
                              "room_count": random.randint(1, 7),
                              "rent_per_room": random.randint(400, 800),
                              "location": {"x": random.randint(0, 100),
                                           "y": random.randint(0, 100)},
                              "distance_from_faculties": {}
                              })

        # ----- Creating faculties
        # --> Creating faculties and faculties position randomly
        for faculty in self.faculty_lst:
            self.faculty_data.append({"name": faculty,
                                      "location": {"x": random.randint(0, 100),
                                                   "y": random.randint(0, 100)}})

        # --> Computing distance vector between every house and every faculty
        distances = []

        for house in self.data:
            for faculty in self.faculty_data:
                distance_vector_x = abs(house["location"]["x"] - faculty["location"]["x"])
                distance_vector_y = abs(house["location"]["y"] - faculty["location"]["y"])

                distance_vector_magnitude = sqrt(distance_vector_x**2 + distance_vector_y**2)

                # --> Record distance vector magnitude
                distances.append(distance_vector_magnitude)
                house["distance_from_faculties"][faculty["name"]] = distance_vector_magnitude

        # --> Normalise every distance for every house
        for house in self.data:
            for faculty in self.faculty_data:
                house["distance_from_faculties"][faculty["name"]] = \
                    (house["distance_from_faculties"][faculty["name"]] - min(distances))/(max(distances) - min(distances))

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
    houses = House_dataset(10)
    print(houses.data)