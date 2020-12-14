
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
        
        # --> Disabling the gurobi console output, set to 1 to enable
        self.model.Params.OutputFlag=0

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

        #print("Model construction completed")

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

        # --> Creating parameter weight variables
        # (can be used to give more importance to certain parameters over other in pair quality determination)
        distance_weight = 1
        shared_single_weight = 1
        waiting_list_weight = 1
        budget_weight = 1

        for student in self.student_dataset.data:
            # --> Creating entry for student in pair quality dictionary
            pair_quality_dict[student["ref"]] = {}

            for house in self.house_dataset.data:
                # --> Creating entry for house in pair quality dictionary
                pair_quality_dict[student["ref"]][house["ref"]] = 0

                # ----- Calculating pair quality for the given student/house pair
                # (The better the pair quality, the higher the returned value)

                # --> Distance from the faculty
                # (value is 1 - distance from faculty cooresponding to studies)
                pair_quality_dict[student["ref"]][house["ref"]] += \
                    1 - house["distance_from_" + student["study"]] * distance_weight

                # --> Shared vs single housing (value is 1 if constraint is met, otherwise 0)
                if student["preference"] == "single" and house["room_count"] == 1 \
                        or student["preference"] == "shared" and house["room_count"] > 1:
                    pair_quality_dict[student["ref"]][house["ref"]] += 1 * shared_single_weight

                # --> Waiting list position
                # (value is 0 for bottom of waiting list, and gradually becomes 1 for the first in line)
                pair_quality_dict[student["ref"]][house["ref"]] += \
                    (self.student_dataset.nb_students - student["waiting_list_pos"])/self.student_dataset.nb_students \
                    * waiting_list_weight

                # --> Housing cost
                # (adds 1, and reduces that if the budget is exceeded, by the percentage of the exceedance)
                if house["rent_per_room"] < student["budget_min"]:
                    pair_quality_dict[student["ref"]][house["ref"]] += \
                        (1 - (student["budget_min"] - house["rent_per_room"])/student["budget_min"]) * budget_weight

                elif house["rent_per_room"] > student["budget_max"]:
                    pair_quality_dict[student["ref"]][house["ref"]] += \
                        (1 - (house["rent_per_room"] - student["budget_max"])/student["budget_max"]) * budget_weight

                else:
                    pair_quality_dict[student["ref"]][house["ref"]] += 1 * budget_weight

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

            self.model.addConstr(supply_constraint == house["room_count"], constraint_name)

    def build_gender_split_constraints(self):
        """
        Used to generate the gender split constraints (1 per house)

            "sum of decisions variables of all female students for a given house >= 2"

        :return: None
        """

        for house in self.house_dataset.data:
            if house["room_count"] > 1:
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

    def optimize(self):
        self.model.optimize()

if __name__ == '__main__':
    from Student_dataset import Student_dataset
    from House_dataset import House_dataset

    # Settings small verification scenario: random.seed(34), 9 students,
    # ae, cs and 2 houses.
    model = Model_generator(Student_dataset(9,["ae", "cs"]), House_dataset(2,
                                                                           ["ae", "cs"]))

    model.output_to_lp()
    model.optimize()
