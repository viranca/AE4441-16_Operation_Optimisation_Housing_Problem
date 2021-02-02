
from House_dataset import House_dataset
from Student_dataset import Student_dataset
from Model_generator import Model_generator
import statistics
import sys
import matplotlib.pyplot as plt

def print_statusline(msg: str):
    last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(msg, end='\r')
    sys.stdout.flush()  # Some say they needed this, I didn't.
    print_statusline.last_msg = msg


def run_model(number_of_students, number_of_houses, statistical_properties):
    Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties)
    House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties)

    #postprocesss script House_dataset1
    #dutch international

    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()

    # #print all x_ij:
    # solution = []   
    # for v in model.model.getVars():
    #       solution.append([v.varName,v.x])
    #print(solution)
    return model.model.ObjVal


"""
=============================================================================
Set inputs and statistical properties for the base model:
=============================================================================
"""

number_of_students = 1000
number_of_houses = 200
number_of_montecarlo_iterations = 600

#The nine properties are:
#room_count, rent_per_room, location, budget_min, year, gender, nationality, study and preference
statistical_properties_base = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties_base)
House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties_base)

"""
#properties to be changable
# #age/year
# Student_dataset1.print_property_stats("year", bin_count=6)
# Student_dataset1.plot_property_histogram("year", bin_count=6)
# Student_dataset1.adjust_property_bin_by_percentage("year", 1, 10, bin_count=6) 
# Student_dataset1.adjust_property_bin_by_percentage("year", 2, 10, bin_count=6) 
# Student_dataset1.adjust_property_bin_by_percentage("year", 3, 10, bin_count=6) 
# Student_dataset1.plot_property_histogram("year", bin_count=6)

# #gender
# Student_dataset1.print_property_stats("gender", bin_count=2)
# Student_dataset1.plot_property_histogram("gender", bin_count=2)
# Student_dataset1.adjust_property_bin_by_percentage("gender", 1, 10, bin_count=2) #towards female
# Student_dataset1.plot_property_histogram("gender", bin_count=2)

# #nationality
# Student_dataset1.print_property_stats("nationality", bin_count=2)
# Student_dataset1.plot_property_histogram("nationality", bin_count=2)
# Student_dataset1.adjust_property_bin_by_percentage("nationality", 1, 10, bin_count=2) #towards dutch
# Student_dataset1.plot_property_histogram("nationality", bin_count=2)

# #study
# Student_dataset1.print_property_stats("study", bin_count=4)
# Student_dataset1.plot_property_histogram("study", bin_count=4)
# Student_dataset1.adjust_property_bin_by_percentage("study", 1, 10, bin_count=4) #towards 3me
# Student_dataset1.adjust_property_bin_by_percentage("study", 2, 10, bin_count=4) #towards ae
# Student_dataset1.adjust_property_bin_by_percentage("study", 3, 10, bin_count=4) #towards cs
# Student_dataset1.adjust_property_bin_by_percentage("study", 4, 10, bin_count=4) #towards io
# Student_dataset1.plot_property_histogram("study", bin_count=4)

# #preference
# Student_dataset1.print_property_stats("preference", bin_count=2)
# Student_dataset1.plot_property_histogram("preference", bin_count=2)
# Student_dataset1.adjust_property_bin_by_percentage("preference", 1, 10, bin_count=2) #towards shared
# Student_dataset1.plot_property_histogram("preference", bin_count=2)


##Property functions
#list_property(self, property)
#print_property_stats(self, property, bin_count=10)
#plot_property_histogram(self, property, bin_count=10)
#adjust_property_bin_by_percentage(self, property, bin_ref, percentage_change, bin_count=10)
#Student_dataset1.plot_property_histogram("year", bin_count=10)
#House_dataset1.plot_property_histogram("preference", bin_count=10)


model = Model_generator(Student_dataset1, House_dataset1)
model.output_to_lp()
model.optimize()
print(model.model.ObjVal)

"""


#%%

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    statistical_properties_base = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

    Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties_base)
    House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties_base)

    #Property changed by postprocessing the generated dataset.
    #age/year
    # Student_dataset1.print_property_stats("year", bin_count=6)
    #Student_dataset1.plot_property_histogram("year", bin_count=6)
    Student_dataset1.adjust_property_bin_by_percentage("year", 1, 10, bin_count=6) 
    Student_dataset1.adjust_property_bin_by_percentage("year", 2, 10, bin_count=6) 
    Student_dataset1.adjust_property_bin_by_percentage("year", 3, 10, bin_count=6) 
    #Student_dataset1.plot_property_histogram("year", bin_count=6)
            
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()
    solutions_model.append(model.model.ObjVal)
    print_statusline('iteration bscplus10: ' + str(i))
print('The objective value for the bscplus10 model equals:' , statistics.mean(solutions_model))  


#%%
solutions_model = []
for i in range(number_of_montecarlo_iterations):
    statistical_properties_base = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

    Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties_base)
    House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties_base)

    # #Property changed by postprocessing the generated dataset.
    #age/year
    #Student_dataset1.print_property_stats("year", bin_count=6)
    #Student_dataset1.plot_property_histogram("year", bin_count=6)
    Student_dataset1.adjust_property_bin_by_percentage("year", 1, -10, bin_count=6) 
    Student_dataset1.adjust_property_bin_by_percentage("year", 2, -10, bin_count=6) 
    Student_dataset1.adjust_property_bin_by_percentage("year", 3, -10, bin_count=6) 
    #Student_dataset1.plot_property_histogram("year", bin_count=6)
        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()
    solutions_model.append(model.model.ObjVal)
    print_statusline('iteration bscmin10: ' + str(i))
print('The objective value for the bscmin10 model equals:' , statistics.mean(solutions_model))  

#%%

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    statistical_properties_base = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

    Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties_base)
    House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties_base)

    # #Property changed by postprocessing the generated dataset.
    # #gender
    # Student_dataset1.print_property_stats("gender", bin_count=2)
    # Student_dataset1.plot_property_histogram("gender", bin_count=2)
    Student_dataset1.adjust_property_bin_by_percentage("gender", 1, 10, bin_count=2) #towards female
    # Student_dataset1.plot_property_histogram("gender", bin_count=2)
        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()
    solutions_model.append(model.model.ObjVal)
    print_statusline('iteration genderplus10: ' + str(i))
print('The objective value for the genderplus10 model equals:' , statistics.mean(solutions_model))  

#%%
solutions_model = []
for i in range(number_of_montecarlo_iterations):
    statistical_properties_base = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

    Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties_base)
    House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties_base)

    # #Property changed by postprocessing the generated dataset.
    # #gender
    # Student_dataset1.print_property_stats("gender", bin_count=2)
    # Student_dataset1.plot_property_histogram("gender", bin_count=2)
    Student_dataset1.adjust_property_bin_by_percentage("gender", 1, -10, bin_count=2) #towards female
    # Student_dataset1.plot_property_histogram("gender", bin_count=2)
    
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()
    solutions_model.append(model.model.ObjVal)
    print_statusline('iteration gendermin10: ' + str(i))
print('The objective value for the gendermin10 model equals:' , statistics.mean(solutions_model))  

#%%
solutions_model = []
for i in range(number_of_montecarlo_iterations):
    statistical_properties_base = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

    Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties_base)
    House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties_base)

    # #Property changed by postprocessing the generated dataset.
    # #nationality
    # Student_dataset1.print_property_stats("nationality", bin_count=2)
    # Student_dataset1.plot_property_histogram("nationality", bin_count=2)
    Student_dataset1.adjust_property_bin_by_percentage("nationality", 1, 10, bin_count=2) #towards dutch
    # Student_dataset1.plot_property_histogram("nationality", bin_count=2)

        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()
    solutions_model.append(model.model.ObjVal)
    print_statusline('iteration nationalityplus10: ' + str(i))
print('The objective value for the nationalityplus10 model equals:' , statistics.mean(solutions_model))  

#%%
solutions_model = []
for i in range(number_of_montecarlo_iterations):
    statistical_properties_base = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

    Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties_base)
    House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties_base)

    #Property changed by postprocessing the generated dataset.
    # #nationality
    # Student_dataset1.print_property_stats("nationality", bin_count=2)
    # Student_dataset1.plot_property_histogram("nationality", bin_count=2)
    Student_dataset1.adjust_property_bin_by_percentage("nationality", 1, -10, bin_count=2) #towards dutch
    # Student_dataset1.plot_property_histogram("nationality", bin_count=2)
        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()
    solutions_model.append(model.model.ObjVal)
    print_statusline('iteration nationalitymin10: ' + str(i))
print('The objective value for the nationalitymin10 model equals:' , statistics.mean(solutions_model))  












































