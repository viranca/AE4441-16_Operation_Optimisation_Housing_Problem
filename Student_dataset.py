
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random

# Libs
import numpy as np
from faker import Faker

# Own modules
from Dataset_abc import Dataset_abc

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '08/11/2020'

################################################################################################################


class Student_dataset(Dataset_abc):
    def __init__(self,
                 nb_students,
                 faculty_lst=["ae", "cs", "3me", "io"]):
        """
        Used to generate a student dataset

        Each student has for properties:
            - Reference number
            - Name (random)
            - Age (random)
            - Gender (random)
            - Nationality (random)
            - Year (random)
            - Study (random)
            - Preference (random)
            - Budget min (normal distribution)
            - Budget max (random)
            - Waiting list position (random)

        :param nb_students: Number of student to be generated
        :param faculty_lst: Faculties available (need to match one provided to House_dataset)
        """

        # --> Initialise abstract class
        super().__init__()

        # --> Initialising records
        self.nb_students = nb_students
        self.faculty_lst = faculty_lst
        self.data = []

        # --> Initialising data properties
        self.statistical_properties = {
                                       # "age": {"mu": 3,
                                       #         "sigma": 1},

                                       "budget_min": {"mu": 300,
                                                      "sigma": 100},

                                       # "budget_max": {"mu": 600,
                                       #                "sigma": 100},
                                       }

        # ----- Generating data
        self.gen_data()

    def gen_data(self):
        """
        Used to generate dataset
        """

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
                              "study": random.choice(self.faculty_lst),
                              "preference": random.choice(["shared", "single"]),
                              "budget_min": int(np.random.normal(self.statistical_properties["budget_min"]["mu"],
                                                                 self.statistical_properties["budget_min"]["sigma"],
                                                                 1)),
                              "budget_max": None,
                              "waiting_list_pos": waiting_list_positions.pop(0)})

        # --> Updating budget_max
        for i in range(len(self.data)):
            self.data[i]["budget_max"] = self.data[i]["budget_min"] + random.randint(150, 300)

        # --> Updating year according to age
        for i in range(len(self.data)):
            if self.data[i]["age"] < 20:
                self.data[i]["year"] = random.randint(1, 3)

            else:
                self.data[i]["year"] = random.randint(3, 7)

        # --> Sorting students by year
        self.sort_by_property("year")


if __name__ == '__main__':
    students = Student_dataset(1000)

    # students.plot_property_histogram("budget_min", bin_count=10)
    # students.plot_property_histogram("budget_max", bin_count=10)
    # students.plot_property_histogram("gender")
    # students.plot_property_histogram("study")

    students.get_property_stats("budget_min")
    students.get_property_stats("study")
