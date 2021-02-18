
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
from Dataset_parent import Dataset

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '08/11/2020'

################################################################################################################


class House_dataset(Dataset):
    def __init__(self,
                 nb_houses,
                 faculty_lst=["ae", "cs", "3me", "io"],
                 statistical_properties=None,
                 x_position_range=(0, 100),
                 y_position_range=(0, 100)):
        """
        Used to generate a house dataset

        Each house has for properties:
            - Reference number
            - Address (random)
            - Room count (normal distribution)
            - Location with sub-properties - x (normal distribution)
                                           - y (normal distribution)
            - Distance from faculties with sub-properties - every faculties from the faculty lst

        :param nb_houses: Number of houses to be generated
        :param faculty_lst (list): Faculties available (need to match one provided to Student_dataset)
        :param statistical_properties (formatted dict): Dict of statistical properties, correctly formatted
        :param x_position_range (tuple): Range of possible x positions of houses
        :param y_position_range (tuple): Range of possible y positions of houses
        """

        # --> Initialise abstract class
        super().__init__()

        # --> Initialising records
        self.nb_houses = nb_houses
        self.faculty_lst = faculty_lst
        self.data = []
        self.faculty_data = []

        # --> Initialising data properties
        if statistical_properties is None:
            self.statistical_properties = {"room_count": {"mu": 3,
                                                          "sigma": 2},

                                           "rent_per_room": {"mu": 600,
                                                             "sigma": 100},

                                           "location": {"mu": 50,
                                                        "sigma": 25}}

        else:
            self.statistical_properties = statistical_properties

        self.x_position_range = x_position_range
        self.y_position_range = y_position_range

        # ----- Generating data
        self.gen_data()

    def gen_data(self):
        # ----- Initialising tools
        fake = Faker()

        # ----- Creating houses
        for i in range(self.nb_houses):
            self.data.append({"ref": str(i),        # ref is made a string to better work with dictionary format adopted
                              "address": fake.address(),
                              "room_count": abs(int(np.random.normal(self.statistical_properties["room_count"]["mu"],
                                                                     self.statistical_properties["room_count"]["sigma"],
                                                                     1))) + 1,

                              "rent_per_room": int(np.random.normal(self.statistical_properties["rent_per_room"]["mu"],
                                                                    self.statistical_properties["rent_per_room"]["sigma"],
                                                                    1)),

                              "x_location": int(np.random.normal(self.statistical_properties["location"]["mu"],
                                                                 self.statistical_properties["location"]["sigma"],
                                                                 1)),

                              "y_location": int(np.random.normal(self.statistical_properties["location"]["mu"],
                                                                 self.statistical_properties["location"]["sigma"],
                                                                 1)),
                              })

        # ----- Creating faculties
        # --> Creating faculties and faculties position randomly
        for faculty in self.faculty_lst:
            self.faculty_data.append({"name": faculty,
                                      "location": {"x": random.randint(self.x_position_range[0], self.x_position_range[1]),
                                                   "y": random.randint(self.y_position_range[0], self.y_position_range[1])}})

        # --> Computing distance vector between every house and every faculty
        distances = []

        for house in self.data:
            for faculty in self.faculty_data:
                distance_vector_x = abs(house["x_location"] - faculty["location"]["x"])
                distance_vector_y = abs(house["y_location"] - faculty["location"]["y"])

                distance_vector_magnitude = sqrt(distance_vector_x**2 + distance_vector_y**2)

                # --> Record distance vector magnitude
                distances.append(distance_vector_magnitude)
                house["distance_from_" + faculty["name"]] = distance_vector_magnitude

        # --> Normalise every distance for every house
        for house in self.data:
            for faculty in self.faculty_data:
                house["distance_from_" + faculty["name"]] = \
                    (house["distance_from_" + faculty["name"]] - min(distances))/(max(distances) - min(distances))

    def change_statisticalproperties(self, new_statistical_properties):
        self.statistical_properties = new_statistical_properties
        
        
if __name__ == '__main__':
    houses = House_dataset(150)
    # print(houses.data)
    # print(houses.list_property("room_count"))

    # houses.plot_property_histogram("room_count", bin_count=7)
    # houses.plot_property_histogram("rent_per_room", bin_count=10)
    houses.plot_property_histogram("distance_from_ae", bin_count=10)
    houses.plot_property_histogram("x_location", bin_count=10)
