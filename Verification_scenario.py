from Student_dataset import Student_dataset
from House_dataset import House_dataset
from Model_generator import Model_generator
from math import sqrt
import copy


def change_house_shared(houses, percent):
    count_single_to_be = int(len(houses.data) * percent)
    count_single = 0
    for house in houses.data:
        if house['room_count'] == 1:
            count_single += 1
    change_count = count_single_to_be - count_single
    for house in houses.data:
        if change_count <= 0:
            break
        if house['room_count'] != 1:
            house['room_count'] = 1
            change_count -= 1

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
    Set up Verification Scenario, 1000 students and 100 houses, 4 faculties, 
    standard statistical properties
    """
    students = Student_dataset(1000, ["ae", "cs", "3me", "io"])

    houses = House_dataset(100, ["ae", "cs", "3me", "io"])

    model = Model_generator(students, houses)
    model.optimize()

    print("Objective value of original dataset: {}".format(model.model.ObjVal))

    print("********Testing faculty movement effect********\n\n")



    """Test moving some houses exactly on top of the faculties average location
    Expected: objective function increases as the distance to faculties 
    should be smaller
    """
    houses2 = copy.deepcopy(houses)
    houses2 = move_some_houses(houses2, 0.3)
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
    houses2 = move_some_houses(houses2, 0.5)
    houses2.plot_property_histogram("x_location", bin_count=10)
    houses2.plot_property_histogram("y_location", bin_count=10)
    model2 = Model_generator(students, houses2)
    model2.optimize()
    print("Objective value of moved houses 2 dataset: {}".format(
        model2.model.ObjVal))
    print("Difference in Objective value of moved houses 2 dataset: {}".format(
        model2.model.ObjVal - model.model.ObjVal))



    """Test decreasing the house costs from mu of 600 to mu of 450 to mu of 300
    Expected: objective function increases
    """
    houses3 = House_dataset(100, ["ae", "cs", "3me", "io"], {"room_count": {
        "mu": 3,
                                                          "sigma": 1},

                                           "rent_per_room": {"mu": 450,
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

    houses3 = House_dataset(100, ["ae", "cs", "3me", "io"], {"room_count": {
        "mu": 3,
                                                          "sigma": 1},

                                           "rent_per_room": {"mu": 300,
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



    """Test increasing the percentage of single housing from 50 percent to 60 to 70 percent
    Expected: objective function increases since the preferences are 50 50 
    and there are more shared houses
    """
    houses4 = copy.deepcopy(houses)
    houses.plot_property_histogram("room_count", bin_count=10)
    houses4 = change_house_shared(houses4, 0.6)
    houses4.plot_property_histogram("room_count", bin_count=10)
    model4 = Model_generator(students, houses4)
    model4.optimize()
    print("Objective value of more single rooms dataset: {}".format(
        model4.model.ObjVal))
    print("Difference in Objective value of more single rooms dataset: {}".format(
        model4.model.ObjVal - model.model.ObjVal))

    houses4 = copy.deepcopy(houses)
    houses4 = change_house_shared(houses4, 0.7)
    houses4.plot_property_histogram("room_count", bin_count=10)
    model4 = Model_generator(students, houses4)
    model4.optimize()
    print("Objective value of more single rooms 2 dataset: {}".format(
        model4.model.ObjVal))
    print("Difference in Objective value of more single rooms dataset: {}".format(
        model4.model.ObjVal - model.model.ObjVal))