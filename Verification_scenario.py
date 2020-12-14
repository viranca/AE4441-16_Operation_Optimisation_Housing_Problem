from Student_dataset import Student_dataset
from House_dataset import House_dataset
from Model_generator import Model_generator
from math import sqrt
import copy

def change_student_shared(students, percent):
    count_shared_to_be = int(len(students.data) * percent)
    count_shared = 0

    for student in students.data:
        if student['preference'] == 'shared':
            count_shared += 1
    change_count = count_shared_to_be - count_shared

    for student in students.data:
        if change_count >= 0:
            if student['preference'] == 'single':
                student['preference'] = 'shared'
                change_count -= 1

    return students

def change_house_shared(houses, percent):
    house_count = len(houses.data)
    count_single_to_be = int(len(houses.data) * percent)
    count_single = 0
    room_count = 0
    for house in houses.data:
        if house['room_count'] == 1:
            count_single += 1
        room_count += house['room_count']
    change_count = count_single_to_be - count_single
    number_of_rooms_after_change = 0
    change_count_before = change_count
    for house in houses.data:
        if change_count >= 0:
            if house['room_count'] != 1:
                house['room_count'] = 1
                change_count -= 1
        number_of_rooms_after_change += house['room_count']

    print("Amount of houses: {}, Amount of single houses: {}, amount of rooms "
          "total: {}\n"
          "amount of houses to become single: {}, amount of rooms total "
          "after change: {}".format(house_count, count_single,
                                                         room_count,
                                                         change_count_before,
                                                         number_of_rooms_after_change))
    return houses

def move_some_houses(houses, percent):
    """
    Used to move some houses on top of the average faculty location.

    :param houses: The houses object from the house_dataset
    :param percent: The percentage of houses you want to move (input in
    decimals; 0.2 = 20%)
    :param distance: Distance in x AND y to move houses closer to avg
    faculty, positive value means closer, negative means further away.

    Calculate average faculty locations in x,y then move a percentage of
    houses will be moved x, y distance in the right direction away or to the
    faculties depending on the location of each house.
    """

    avg_x = 0
    avg_y = 0
    number_of_faculties = len(houses.faculty_lst)
    """Get average x,y position of faculties"""
    for faculty in houses.faculty_data:
        avg_x += faculty['location']['x']
        avg_y += faculty['location']['y']
    avg_x /= number_of_faculties
    avg_y /= number_of_faculties
    print("average x: {}, average y: {}".format(avg_x, avg_y))

    number_of_houses = len(houses.data)
    """Move percentage of houses to average faculty location"""
    for i in range(int(number_of_houses*percent)):
        houses.data[i]['x_location'] = avg_x
        houses.data[i]['y_location'] = avg_y

    # --> Recompute distance vector between every house and every faculty
    distances = []

    for house in houses.data:
        for faculty in houses.faculty_data:
            distance_vector_x = abs(
                house["x_location"] - faculty["location"]["x"])
            distance_vector_y = abs(
                house["y_location"] - faculty["location"]["y"])

            distance_vector_magnitude = sqrt(
                distance_vector_x ** 2 + distance_vector_y ** 2)

            # --> Record distance vector magnitude
            distances.append(distance_vector_magnitude)
            house["distance_from_" + faculty[
                "name"]] = distance_vector_magnitude

    # --> Normalise every distance for every house
    for house in houses.data:
        for faculty in houses.faculty_data:
            house["distance_from_" + faculty["name"]] = \
                (house["distance_from_" + faculty["name"]] - min(
                    distances)) / (max(distances) - min(distances))

    return houses

if __name__ == '__main__':
    """
    Set up Verification Scenario, 8000 students and 800 houses and 
    4 faculties, standard statistical properties
    """
    n_students = 8000
    n_houses = 800
    faculties = ["ae", "cs", "3me", "io"]
    students = Student_dataset(n_students, faculties)

    houses = House_dataset(n_houses, faculties)

    model = Model_generator(students, houses)
    model.optimize()

    print("Objective value of original dataset: {}".format(model.model.ObjVal))

    print("********Testing faculty movement effect********\n\n")



    """Test moving some houses exactly on top of the faculties average location
    Expected: objective function increases as the distance to faculties
    should be smaller
    """
    houses2 = copy.deepcopy(houses)
    houses2 = move_some_houses(houses2, 0.15)
    model2 = Model_generator(students, houses2)
    model2.optimize()
    print("Objective value of moved houses dataset: {}".format(
        model2.model.ObjVal))
    print("Difference in Objective value of moved houses dataset: {}".format(
        model2.model.ObjVal - model.model.ObjVal))
    houses.plot_property_histogram("x_location", bin_count=10)
    houses2.plot_property_histogram("x_location", bin_count=10)
    houses.plot_property_histogram("y_location", bin_count=10)
    houses2.plot_property_histogram("y_location", bin_count=10)

    houses2 = copy.deepcopy(houses)
    houses2 = move_some_houses(houses2, 0.3)
    houses2.plot_property_histogram("x_location", bin_count=10)
    houses2.plot_property_histogram("y_location", bin_count=10)
    model2 = Model_generator(students, houses2)
    model2.optimize()
    print("Objective value of moved houses 2 dataset: {}".format(
        model2.model.ObjVal))
    print("Difference in Objective value of moved houses 2 dataset: {}".format(
        model2.model.ObjVal - model.model.ObjVal))



    """Test decreasing the house costs from mu of 600 to mu of 500 to mu of 400
    Expected: objective function increases
    """
    houses3 = House_dataset(n_houses, faculties, {"room_count": {
        "mu": 3,
        "sigma": 1},

        "rent_per_room": {"mu": 600,
                          "sigma": 100},

        "location": {"mu": 50,
                     "sigma": 25}})
    houses.plot_property_histogram("rent_per_room", bin_count=10)
    houses3.plot_property_histogram("rent_per_room", bin_count=10)
    model3 = Model_generator(students, houses3)
    model3.optimize()
    print("Objective value of original dataset for rent change"
          ": {}, should be equal to: {}".format(model3.model.ObjVal,
                                                model.model.ObjVal))

    houses3 = House_dataset(n_houses, faculties, {"room_count": {
        "mu": 3,
                                                          "sigma": 1},

                                           "rent_per_room": {"mu": 500,
                                                             "sigma": 100},

                                           "location": {"mu": 50,
                                                        "sigma": 25}})
    houses.plot_property_histogram("rent_per_room", bin_count=10)
    houses3.plot_property_histogram("rent_per_room", bin_count=10)
    model3 = Model_generator(students, houses3)
    model3.optimize()


    print("Objective value of cheaper rent dataset: {}".format(
        model3.model.ObjVal))
    print("Difference in Objective value of cheaper rent dataset: {}".format(
        model3.model.ObjVal - model.model.ObjVal))

    houses3 = House_dataset(n_houses, faculties, {"room_count": {
        "mu": 3,
                                                          "sigma": 1},

                                           "rent_per_room": {"mu": 400,
                                                             "sigma": 100},

                                           "location": {"mu": 50,
                                                        "sigma": 25}})
    houses3.plot_property_histogram("rent_per_room", bin_count=10)
    model3 = Model_generator(students, houses3)
    model3.optimize()
    print("Objective value of cheaper rent 2 dataset: {}".format(
        model3.model.ObjVal))
    print("Difference in Objective value of cheaper rent 2 dataset: {}".format(
        model3.model.ObjVal - model.model.ObjVal))



    """Test increasing the percentage of single housing to 30% and 50%
    Expected: objective function decreases since there are less rooms available
    """
    houses4 = copy.deepcopy(houses)
    houses.plot_property_histogram("room_count", bin_count=10)
    houses4 = change_house_shared(houses4, 0.15)
    houses4.plot_property_histogram("room_count", bin_count=10)
    model4 = Model_generator(students, houses4)
    model4.optimize()
    print("Objective value of more single rooms dataset: {}".format(
        model4.model.ObjVal))
    print("Difference in Objective value of more single rooms dataset: {}".format(
        model4.model.ObjVal - model.model.ObjVal))

    houses4 = copy.deepcopy(houses)
    houses4 = change_house_shared(houses4, 0.3)
    houses4.plot_property_histogram("room_count", bin_count=10)
    model4 = Model_generator(students, houses4)
    model4.optimize()
    print("Objective value of more single rooms 2 dataset: {}".format(
        model4.model.ObjVal))
    print("Difference in Objective value of more single rooms dataset: {}".format(
        model4.model.ObjVal - model.model.ObjVal))

    """Test increasing the percentage of shared vs single housing student
    preference from 50 percent to 60 to 70 percent of students preferring 
    shared housing
    Expected: objective function increases since the preferences are 50 50 
    and there are more shared houses than there are single houses
    """
    students.plot_property_histogram("preference")
    students1 = copy.deepcopy(students)
    students1 = change_student_shared(students1, 0.6)
    students1.plot_property_histogram("preference")
    model5 = Model_generator(students1, houses)
    model5.optimize()
    print("Objective value of more shared preference dataset: {}".format(
        model5.model.ObjVal))
    print("Difference in Objective value of more shared preference dataset: {}".format(
        model5.model.ObjVal - model.model.ObjVal))

    students2 = copy.deepcopy(students)
    students2 = change_student_shared(students1, 0.7)
    students2.plot_property_histogram("preference")
    model6 = Model_generator(students2, houses)
    model6.optimize()
    print("Objective value of more shared preference 2 dataset: {}".format(
        model6.model.ObjVal))
    print("Difference in Objective value of more shared preference dataset: {}".format(
        model6.model.ObjVal - model.model.ObjVal))

