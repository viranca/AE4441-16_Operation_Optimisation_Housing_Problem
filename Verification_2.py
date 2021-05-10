from Student_dataset import Student_dataset
from House_dataset import House_dataset
from Model_generator import Model_generator
import random
import numpy as np
import copy

if __name__ == '__main__':

    # random.seed = 2

    # print("Random seed is: ", random.seed)

    student_data = Student_dataset(4)
    house_data = House_dataset(2)

    """Information about students and houses"""
    print(house_data.nb_houses)
    print(student_data.nb_students)

    model = Model_generator(student_data, house_data)

    model.output_to_lp()
    model.optimize()

    orig_vars = [model.model.ObjVal]
    model.model.printAttr('X')
    X = model.model.getAttr('X')
    # Obj = model.model.getAttr('Obj')

    """Testing hard constraints"""
    # Demand; a student can only be in one house
    # Unit test by going through all decision variables and make sure that a student can only be in one house;
    # cut the decision variables to the first nb_houses * nb_students,
    # split this cut list into a chunk of lists with length of nb_students
    # check for each of these chunks if the count of 1 is larger than 1, if true the demand constraint is not met.
    X_demand = X[0:house_data.nb_houses * student_data.nb_students]
    X_demand = np.array_split(X_demand, student_data.nb_students)

    for x in X_demand:
        if x.tolist().count(1) > 1:
            print("Demand constraint not satisfied")

    # Supply upper bound; the capacity of a house cannot be exceeded
    # Unit test by making a list of all the room counts,
    # then going through the decision variables chunks created earlier and subtracting 1 from the right room count each time a student is in a house
    house_rooms = []
    for house in house_data.data:
        house_rooms.append(house['room_count'])

    house_rooms_upper = copy.deepcopy(house_rooms)
    for x in X_demand:
        if x.tolist().count(1) == 1:
            house_rooms_upper[x.tolist().index(1)] -= 1

    for house_room in house_rooms_upper:
        if house_room < 0:
            print("Supply upper bound constraint not satisfied")


    # 1st year priority; first year students must be given a room
    # This is a unit test where a list of zeros is made of len of all students,
    # and first year student indices are set to 1. Then a check is done if
    # all the first year students' decision variables have a count of 1.
    fyp_students = [0]*student_data.nb_students
    i = 0
    for student in student_data.data:
        if student['year'] == 1:
            fyp_students[i] = 1
        i += 1

    i = 0
    for x in X_demand:
        first_year_student = fyp_students[i]
        if first_year_student == 1 and x.tolist().count(1) != 1:
            print("First year priority constraint not satisfied")
        i += 1

    # Gender split; a shared house must have 0 or 2 or more females
    # This constraint is checked by unit test. Same as with first years a list of students with females listed as 1 and males as 1 is made. Now a list of number of females is made in each house, initially set to 0.
    # Then a loop is done through the chunked decision variables and going through all houses with more than 1 room and adding a female to the correct index of list of females(if decision variable is female).
    # Finally the check is made if females list is larger than or equal to 2 for all indices.
    female_students = [0]*student_data.nb_students
    i = 0
    for student in student_data.data:
        if student['gender'] == 'f':
            female_students[i] = 1
        i += 1
    i = 0
    nb_females = [0]*house_data.nb_houses
    for x in X_demand:
        female = female_students[i]
        if female == 1:
            if x.tolist().count(1) == 1:
                nb_females[x.tolist().index(1)] += 1
    i += 1

    i = 0
    for nb_females_in_house in nb_females:
        if house_rooms[i] > 1:
            if nb_females_in_house == 0:  # 0 females
                continue
            if nb_females_in_house == 1:  # 2 or more satisfied
                print("Gender split constraint not satisfied")
        i += 1

    """Soft"""
    # For the soft constraints the model was ran with certain parameters and
    # the resulting optimal objective function was checked manually to see
    # if the soft constraints were applied correctly.

    # Supply lower bound; a house will be filled at less than max capacity for a penalty
    # Run a model with 5 students and 5 houses and check if the softness was applied.
    # In one run all the 5 houses had more than 1 room, and the model chose to fill the 3rd and the 5th house, which had 2 and 3 rooms, respectively. Thereby, the penalty was reduced to 3 houses, instead of all 5.

    # Study; house with multiple studies inside will have a penalty
    # Test by checking if a house with multiple studies inside gets the penalty.
    # This was done by generating 4 students where all students had a different
    # studies and 2 house each with 2 rooms. The model is then ran and checked.
    # student_data = Student_dataset(3)
    # house_data = House_dataset(1)
    # house_data.data[0]['room_count'] = 3
    # # house_data.data[1]['room_count'] = 2
    # student_data.data[0]['study'] = student_data.faculty_lst[0]
    # student_data.data[1]['study'] = student_data.faculty_lst[0]
    # student_data.data[2]['study'] = student_data.faculty_lst[2]
    # # student_data.data[3]['study'] = student_data.faculty_lst[3]
    #
    # """Information about students and houses"""
    # print(house_data.nb_houses)
    # print(student_data.nb_students)
    #
    # model = Model_generator(student_data, house_data)
    #
    # model.output_to_lp()
    # model.optimize()
    #
    # orig_vars = [model.model.ObjVal]
    # model.model.printAttr('X')

    # Dutch; a house can be mixed with Dutch and international students for a penalty
    # Test by checking if a house with multiple nationalities inside get the penalty.



    """Testing the pair quality"""
    # For the testing of the pair quality,
    # the reader is encouraged to look at the last section's example.
    # Where the summation of pair values per preference is shown for Michelle.

    """Testing constraints implementation"""
    # To verify that all the constraints have been added, the lp file was outputted and can be seen in appendix A.
    # The
