
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random

# Libs
import numpy as np
from faker import Faker
import gurobipy as gp
from gurobipy import GRB

# Own modules
from Student_dataset import Student_dataset
from House_dataset import House_dataset

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '19/11/2020'

################################################################################################################


class Model_generator:
    def __init__(self, student_data, house_data):
        # --> Setting up records
        self.student_dataset = student_data
        self.house_dataset = house_data

        # ---- Creating model
        self.model = gp.Model("OO_assignment_model")

        # --> Preforming data pre-processing
        self.pair_quality_dict, self.decision_variable_dict = self.pre_process_data()
        self.model.update()

        # --> Building objective function
        self.build_objective()

        # --> Setting up constraints
        self.build_demand_constraints()
        self.build_supply_constraints()
        self.build_gender_split_constraints()
        self.build_first_year_priority_constraint()

        print("Model construction completed")

    def pre_process_data(self):
        """
        Used ot generate the pair quality based on student preference and house properties, amd decision variables for
        each student/house pair.

        Both are arranged in a dictionary {student ref: {house ref: ...} }

        :return: pair_quality_dict, decision_variable_dict
        """

        # ========================== Pair quality dictionary generation =====================
        # --> Compute pair quality matrix for all student/house pair
        pair_quality_dict = {}

        # waiting_list_weight = 10
        # preference_weight = 10

        for student in self.student_dataset.data:
            # --> Creating entry for student in pair quality dictionary
            pair_quality_dict[student["ref"]] = {}

            for house in self.house_dataset.data:
                # --> Creating entry for student in pair quality dictionary                
                pair_quality_dict[student["ref"]][house["ref"]] = 0
            
                # --> Calculating pair quality for the given student/house pair
                # --> The better the pair quality, the higher the returned value.
                # --> Shared vs single housing (value is 1 if contraint is met, otherwise 0)
                # --> TODO                
                if student["preference"] == "single" and house["room_count"] == 1:
                    pair_quality_dict[student["ref"]][house["ref"]] += 1
                if student["preference"] == "shared" and house["room_count"] > 1:
                    pair_quality_dict[student["ref"]][house["ref"]] += 1                
                # --> Waiting list position (value is 0 for bottom of waiting list, and gradually becomes 1 for the first in line.)
                #print("Is this the amount of students?", self.student_dataset.nb_students)
                pair_quality_dict[student["ref"]][house["ref"]] += (self.student_dataset.nb_students - student["waiting_list_pos"])/self.student_dataset.nb_students
                # --> Housing cost (adds 1, and reduces that if the budget is exceeded, by the percentage of the exceedance.)
                pair_quality_dict[student["ref"]][house["ref"]] += 1 
                if house["rent_per_room"] < student["budget_min"]:
                    pair_quality_dict[student["ref"]][house["ref"]] -= (student["budget_min"] - house["rent_per_room"])/student["budget_min"] 
                if house["rent_per_room"] > student["budget_min"]: 
                    pair_quality_dict[student["ref"]][house["ref"]] -= (house["rent_per_room"] - student["budget_max"])/student["budget_max"]                    
                

                # pair_quality_dict[student["ref"]][house["ref"]] = \
                #     - abs(student["budget_max"] - house["rent_per_room"]) \
                #     - student["waiting_list_pos"] * waiting_list_weight \
                #     - (student["preference"] == "single") * (house["room_count"] - 1) * preference_weight
                    
        print(pair_quality_dict)
        
        
        
        
        # ========================== Decision variable dictionary generation =================
        # --> Creating decision variable dictionary
        decision_variable_dict = {}

        for student in self.student_dataset.data:
            # --> Creating entry for student in decision variable dictionary
            decision_variable_dict[student["ref"]] = {}

            for house in self.house_dataset.data:
                # --> Creating entry for student in decision variable dictionary
                decision_variable_dict[student["ref"]][house["ref"]] = None

                # --> Generating decision variable name according to convention x_student-ref_house-ref
                variable_name = "x_" + str(student["ref"]) + "_" + str(house["ref"])

                # --> Creating and recording decision variable for corresponding pair in decision variable dictionary
                decision_variable_dict[student["ref"]][house["ref"]] = \
                    self.model.addVar(vtype=GRB.BINARY, name=variable_name)
        #print(decision_variable_dict)
        
        return pair_quality_dict, decision_variable_dict

    def build_objective(self):
        """
        Used to generate the objective function of the model

        :return: None
        """

        # --> Initiating objective function linear expression
        objective_function = gp.LinExpr()

        # --> Adding decision variables for each student/house combination multiplied by their respective pair quality
        for student in self.student_dataset.data:
            for house in self.house_dataset.data:
                # --> Adding variable to model with pair quality
                objective_function += self.decision_variable_dict[student["ref"]][house["ref"]] \
                    * self.pair_quality_dict[student["ref"]][house["ref"]]

        # --> Setting objective
        self.model.setObjective(objective_function, GRB.MAXIMIZE)

    def build_demand_constraints(self):
        """
        Used to generate the demand constraints (1 per student)

            "sum of decisions variables of all houses for a given student <= 1"

        :return: None
        """

        for student in self.student_dataset.data:
            # --> Generating constraint name according to convention C_demand_student-ref
            constraint_name = "C_demand_" + str(student["ref"])

            # --> Adding all decision variables (corresponding to given student) to constraint
            demand_constraint = gp.LinExpr()

            for house in self.house_dataset.data:
                demand_constraint += self.decision_variable_dict[student["ref"]][house["ref"]]

            self.model.addConstr(demand_constraint <= 1, constraint_name)

    def build_supply_constraints(self):
        """
        Used to generate the supply constraints (1 per student)

            "sum of decisions variables of all students for a given house <= given house capacity"

        :return: None
        """

        for house in self.house_dataset.data:
            # --> Generating constraint name according to convention C_supply_house-ref
            constraint_name = "C_supply_" + str(house["ref"])

            # --> Adding all decision variables (corresponding to given house) to constraint
            supply_constraint = gp.LinExpr()

            for student in self.student_dataset.data:
                supply_constraint += self.decision_variable_dict[student["ref"]][house["ref"]]

            self.model.addConstr(supply_constraint <= house["room_count"], constraint_name)

    def build_gender_split_constraints(self):
        """
        Used to generate the gender split constraints (1 per house)

            "sum of decisions variables of all female students for a given house >= 2"

        :return: None
        """

        for house in self.house_dataset.data:
            # --> Generating constraint name according to convention C_gs_house-ref
            constraint_name = "C_gs_" + str(house["ref"])

            # --> Adding all decision variables (corresponding to given house) to constraint
            gs_constraint = gp.LinExpr()

            for student in self.student_dataset.data:
                if student["gender"] == "f":
                    gs_constraint += self.decision_variable_dict[student["ref"]][house["ref"]]

            self.model.addConstr(gs_constraint >= 2, constraint_name)

    def build_first_year_priority_constraint(self):
        """
        Used to generate 1st year student priority constraint (1 constraint)

            "sum of 1st year student decision variables = nb of 1st year students"

        :return: None
        """
        # --> Adding all decision variables (corresponding to 1st year students) to constraint
        fyp_constraint = gp.LinExpr()

        fy_students_count = 0

        for student in self.student_dataset.data:
            if student["year"] == 1:
                fy_students_count += 1

                for house in self.house_dataset.data:
                    fyp_constraint += self.decision_variable_dict[student["ref"]][house["ref"]]

        self.model.addConstr(fyp_constraint == fy_students_count, "fyp")

    def output_to_lp(self):
        """
        Used to generate an LP fiule from the generated model

        :return: None
        """

        self.model.write("Model.lp")

    def optimise(self):
        self.model.optimise()

if __name__ == '__main__':
    from Student_dataset import Student_dataset
    from House_dataset import House_dataset

    model = Model_generator(Student_dataset(10), House_dataset(10))
    model.output_to_lp()