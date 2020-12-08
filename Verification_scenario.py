from Student_dataset import Student_dataset
from House_dataset import House_dataset
from Model_generator import Model_generator
from math import sqrt

def move_faculties_closer_to_houses(houses, percent):
    """
    Move faculties closer to average house location
    percent should be given in decimals, so 20% = 0.2 input

    Once the average house locations in x,y are known, the distance per
    faculty to the average house location is found. Then, the input
    percentage is used on this distance (s.t. if percent is 100% the faculty
    is moved directly on top of the average house location)
    """

    avg_x = 0
    avg_y = 0
    number_of_houses = len(houses.data)
    """Get average x,y position of houses"""
    for house in houses.data:
        avg_x += house['location']['x']
        avg_y += house['location']['y']
    avg_x /= number_of_houses
    avg_y /= number_of_houses
    print("average x: {}, average y: {}".format(avg_x,avg_y))

    """Move faculties percentage wise closer to average house locations"""
    for faculty in houses.faculty_data:
        distance_faculty_avg_house_x = abs(faculty['location']['x'] - avg_x)
        distance_faculty_avg_house_y = abs(faculty['location']['y'] - avg_y)
        print(distance_faculty_avg_house_x,distance_faculty_avg_house_y)
        print("Original Faculty name: {}, (x,y):({},{})".format(
            faculty['name'],faculty['location']['x'],faculty['location']['y']))
        if avg_x > faculty['location']['x']:
            faculty['location']['x'] += distance_faculty_avg_house_x*percent
        else:
            faculty['location']['x'] -= distance_faculty_avg_house_x*percent
        if avg_y > faculty['location']['y']:
            faculty['location']['y'] += distance_faculty_avg_house_y*percent
        else:
            faculty['location']['y'] -= distance_faculty_avg_house_y*percent
        print("Changed Faculty name: {}, (x,y):({},{})".format(faculty['name'],
                                                         faculty['location'][
                                                             'x'],faculty['location']['y']))

        # Recalculate house distances
        # --> Computing distance vector between every house and every faculty
        distances = []

        for house in houses.data:
            for faculty in houses.faculty_data:
                distance_vector_x = abs(
                    house["location"]["x"] - faculty["location"]["x"])
                distance_vector_y = abs(
                    house["location"]["y"] - faculty["location"]["y"])

                distance_vector_magnitude = sqrt(
                    distance_vector_x ** 2 + distance_vector_y ** 2)

                # --> Record distance vector magnitude
                distances.append(distance_vector_magnitude)
                house["distance_from_faculties"][
                    faculty["name"]] = distance_vector_magnitude

        # --> Normalise every distance for every house
        for house in houses.data:
            for faculty in houses.faculty_data:
                house["distance_from_faculties"][faculty["name"]] = \
                    (house["distance_from_faculties"][faculty["name"]] - min(
                        distances)) / (max(distances) - min(distances))
    return houses

if __name__ == '__main__':
    students = Student_dataset(100, ["ae"])
    students.get_property_stats("budget_min")
    students.get_property_stats("study")

    houses = House_dataset(10, ["ae"])
    houses.plot_property_histogram("distance_from_faculties",
                                   sub_property="ae", bin_count=10)
    houses.plot_property_histogram("location", sub_property="x",
                                   bin_count=10)

    model = Model_generator(students, houses)
    model.optimize()

    print("********Testing faculty movement effect********\n\n")

    """Test move faculties closer to average house location effect
    Expected: objective function increases as the distance to faculties 
    should be lower
    """
    houses2 = move_faculties_closer_to_houses(houses, 1)
    model2 = Model_generator(students, houses2)
    model2.optimize()
    houses.plot_property_histogram("distance_from_faculties",
                                   sub_property="ae", bin_count=10)
    houses.plot_property_histogram("location", sub_property="x",
                                   bin_count=10)
    """Test decreasing the house costs
    Expected: objective function increases
    """
    # houses3 = increase_house_price(houses, 0.1)
