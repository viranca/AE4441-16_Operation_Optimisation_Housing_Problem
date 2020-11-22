
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


class Student_dataset:
    def __init__(self, nb_students):
        # ----- Initialising tools

        # --> Seeding generators
        random.seed(345)

        # --> Initialising records
        self.nb_students = nb_students
        self.data = []

        self.gen_data()

    def gen_data(self):
        # ----- Initialising tools
        fake = Faker()

        # --> initializing random waiting list positions 
        waiting_list_positions = [*range(self.nb_students)]
        random.shuffle(waiting_list_positions)
        
        # --> Creating students        
        for i in range(self.nb_students):
            self.data.append({"ref": str(i),
                              "name": fake.name().replace(" ", "_"),
                              "age": random.randint(18, 26),
                              "gender": random.choice(["m", "f"]),
                              "nationality": random.choice(["Dutch", "International"]),
                              "year": None,
                              "study": random.choice(["ae", "cs", "3me"]),
                              "background": random.choice(["dutch", "international"]),

                              "preference": random.choice(["shared", "single"]),
                              "budget_min": random.randint(250, 350),
                              "budget_max": random.randint(400, 700),
                              "waiting_list_pos": waiting_list_positions.pop(0)})

        # --> Updating year according to age
        for i in range(len(self.data)):
            if self.data[i]["age"] < 20:
                self.data[i]["year"] = random.randint(1, 3)

            else:
                self.data[i]["year"] = random.randint(3, 7)

        # --> Sorting students by year
        self.sort_by_property("year")

        # # --> Updating waiting list position
        # for i in range(len(self.data)):
        #     self.data[len(self.data) - i - 1]["waiting_list_pos"] = i + 1

    def list_property(self, property):
        property_lst = []

        for i in range(len(self.data)):
            property_lst.append(self.data[i][property])

        return property_lst

    def sort_by_property(self, property):
        # --> Sorting using insertion sort (smallest to largest)

        for j in range(1, len(self.data)):
            for i in range(j, 0, -1):
                if self.data[i][property] < self.data[i - 1][property]:
                    self.data[i][property], self.data[i - 1][property] = \
                        self.data[i - 1][property], self.data[i][property]


if __name__ == '__main__':
    students = Student_dataset(10)
    print(students.list_property("waiting_list_pos"))
    students.sort_by_property("age")
    print(students.list_property("waiting_list_pos"))
    
