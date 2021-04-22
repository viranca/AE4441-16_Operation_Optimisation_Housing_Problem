
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

        self.decision_variable_dict = {"x": {},
                                       "y": {}}

        # ---- Creating model
        self.model = gp.Model("OO_assignment_model")
        
        # --> Disabling the gurobi console output, set to 1 to enable
        self.model.Params.OutputFlag=0

        # --> Preforming data pre-processing
        self.pair_quality_dict = self.pre_process_data()
        self.model.update()

        # --> Setting up constraints
        self.build_demand_constraints()
        self.build_supply_constraints()
        self.build_gender_split_constraints()
        self.build_first_year_priority_constraint()
        self.build_studies_constraint()

        # --> Building objective function
        self.build_objective()

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
                # (value is 1 - distance from faculty corresponding to studies)
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
        # --> Adding decision variables dictionary

        for student in self.student_dataset.data:
            # --> Creating entry for student in decision variable dictionary
            self.decision_variable_dict["x"][student["ref"]] = {}

            for house in self.house_dataset.data:
                # --> Creating entry for student in decision variable dictionary
                self.decision_variable_dict["x"][student["ref"]][house["ref"]] = None

                # --> Generating decision variable name according to convention x_student-ref_house-ref
                variable_name = "x_" + str(student["ref"]) + "_" + str(house["ref"])

                # --> Creating and recording decision variable for corresponding pair in decision variable dictionary
                self.decision_variable_dict["x"][student["ref"]][house["ref"]] = \
                    self.model.addVar(vtype=GRB.BINARY, name=variable_name)
                    
        return pair_quality_dict

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
                objective_function += self.decision_variable_dict["x"][student["ref"]][house["ref"]] \
                    * self.pair_quality_dict[student["ref"]][house["ref"]]

        # --> Adding all other variables
        # objective_function = self.recursive_add_to_linear_expression(self.decision_variable_dict["y"],
        #                                                              objective_function)

        # for house in self.decision_variable_dict["y"]:
        #     sub_expression = self.recursive_add_to_linear_expression(house, gp.LinExpr())
        #
        #     house_room_count =
        #
        #     sub_expression = (sub_expression - 1) * self.house_dataset.data

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
            constraint = gp.LinExpr()

            for house in self.house_dataset.data:
                constraint += self.decision_variable_dict["x"][student["ref"]][house["ref"]]

            self.model.addConstr(constraint <= 1, constraint_name)

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
            constraint = gp.LinExpr()

            for student in self.student_dataset.data:
                constraint += self.decision_variable_dict["x"][student["ref"]][house["ref"]]

            self.model.addConstr(constraint == house["room_count"], constraint_name)

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
                constraint = gp.LinExpr()

                for student in self.student_dataset.data:
                    if student["gender"] == "f":
                        constraint += self.decision_variable_dict["x"][student["ref"]][house["ref"]]

                self.model.addConstr(constraint >= 2, constraint_name)

    def build_first_year_priority_constraint(self):
        """
        Used to generate 1st year student priority constraint (1 constraint)

            "sum of 1st year student decision variables = nb of 1st year students"

        :return: None
        """
        # --> Adding all decision variables (corresponding to 1st year students) to constraint
        constraint = gp.LinExpr()

        fy_students_count = 0

        for student in self.student_dataset.data:
            if student["year"] == 1:
                fy_students_count += 1

                for house in self.house_dataset.data:
                    constraint += self.decision_variable_dict["x"][student["ref"]][house["ref"]]

        self.model.addConstr(constraint == fy_students_count, "C_fyp")

    def build_nationality_constraint(self):

        return

    def build_studies_constraint(self):
        """

        :return:
        """

        for house in self.house_dataset.data:
            if house["room_count"] > 1:
                # --> Creating house entry in decision_variable_dict
                self.decision_variable_dict["y"][house["ref"]] = {}

                # --> Creating list of study constraints corresponding to study
                for study in self.student_dataset.faculty_lst:
                    # --> Creating study entry in decision_variable_dict[house]
                    self.decision_variable_dict["y"][house["ref"]][study] = {}

                    # --> Generating constraint name according to convention C_gs_house-ref
                    constraint_name = "C_study_" + study + "_" + str(house["ref"])

                    # --> Adding all decision variables (corresponding to given house) to constraint
                    constraint = gp.LinExpr()

                    for student in self.student_dataset.data:
                        if student["study"] == study:
                            constraint += self.decision_variable_dict["x"][student["ref"]][house["ref"]]

                    # --> Creating and recording decision variable for corresponding K out of N constraint
                    self.decision_variable_dict["y"][house["ref"]][study] = \
                        self.model.addVar(vtype=GRB.BINARY, name="y_study_" + study + "_" + str(house["ref"]))

                    # --> Creating summation of student in house must have the same study constraint
                    self.model.addConstr(constraint >= house["room_count"]
                                         - house["room_count"] * self.decision_variable_dict["y"][house["ref"]][study],
                                         constraint_name)

                # --> Creating K (= 1) out of N (= nb. of studies available) constraint
                constraint = self.recursive_add_to_linear_expression(self.decision_variable_dict["y"][house["ref"]],
                                                                     gp.LinExpr())

                self.model.addConstr(constraint == 1, "Study_K_of_N_" + house["ref"])

        return

    def recursive_add_to_linear_expression(self, decision_variable_dict, linear_expression):
        """
        Recursively add all the variables stored in a dictionary to a gurobi linear expression

        :param decision_variable_dict: Dictionary to be recursively iterated through
        :param linear_expression: Linear expression to append to
        :return: augmented linear expression
        """

        for _, variable in decision_variable_dict.items():
            if isinstance(variable, dict):
                self.recursive_add_to_linear_expression(variable, linear_expression)
            else:
                if variable is not None:
                    linear_expression += variable
        return linear_expression

    def output_to_lp(self):
        """
        Used to generate an LP file from the generated model

        :return: None
        """

        self.model.write("Model.lp")

    def optimize(self):
        self.model.optimize()


if __name__ == '__main__':
    from Student_dataset import Student_dataset
    from House_dataset import House_dataset

    model = Model_generator(Student_dataset(100), House_dataset(15))
    model.output_to_lp()
    model.optimize()



