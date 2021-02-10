
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
    sys.stdout.flush()  
    print_statusline.last_msg = msg


def run_model(number_of_students, number_of_houses, statistical_properties):
    Student_dataset1 = Student_dataset(number_of_students, statistical_properties=statistical_properties)
    House_dataset1 = House_dataset(number_of_houses, statistical_properties=statistical_properties)

    #postprocesss script House_dataset1
    #dutch international

    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)
    
    return model, solution_i, allocated_i, model.model.objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev

"""
=============================================================================
Set inputs and statistical properties for the base model:
=============================================================================
"""

number_of_students = 100
number_of_houses = 15
number_of_montecarlo_iterations = 300

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

    


#%%        
            
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


"""
=============================================================================
define the function that runs the model, and run the base model:
=============================================================================
"""




solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students, 
                                                                                        number_of_houses, statistical_properties_base)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration base model: ' + str(i))
print('The objective value for the base model equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))   

    
#%%

"""
=============================================================================
Compute the coefficient of variance and find the required number of MC iterations:
=============================================================================
"""

Coeff_variance = []
for i in range(len(solutions_base_model)):
    mean_upto_i = statistics.mean(solutions_base_model[0:i+2])
    stdev_upto_i = statistics.stdev(solutions_base_model[0:i+2])
    Coeff_variance_i = stdev_upto_i/mean_upto_i
    Coeff_variance.append(Coeff_variance_i)
    
plt.plot(range(len(Coeff_variance)), Coeff_variance)
plt.ylabel('Coefficient of variance Total Fuel Used')
plt.xlabel('Iteration')
plt.show()
#Base model converges after 600 iterations



#%%

"""
=============================================================================
Below is a sequence of simulation setups for the sensitivity analysis of the various parameters.
Each is tested with +10% and -10% from the base model.
=============================================================================
"""

statistical_properties_roomcountplus10 = {"room_count": {"mu": 3.3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}



solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students,
                                                                          number_of_houses, statistical_properties_roomcountplus10)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration roomcountplus10: ' + str(i))
print('The objective value for the roomcountplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))


#%%

statistical_properties_roomcountmin10 = {"room_count": {"mu": 2.7,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students,
                                                                          number_of_houses, statistical_properties_roomcountmin10)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration roomcountmin10: ' + str(i))
print('The objective value for the roomcountmin10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i)) 

#%%

statistical_properties_rentplus10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 660,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students,
                                                                          number_of_houses, statistical_properties_rentplus10)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration rentplus10: ' + str(i))
print('The objective value for the rentplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))  

#%%

statistical_properties_rentmin10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 540,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students,
                                                                          number_of_houses, statistical_properties_rentmin10)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration rentmin10: ' + str(i))
print('The objective value for the rentmin10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i)) 

#%%

statistical_properties_locationplus10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 55,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students,
                                                                          number_of_houses, statistical_properties_locationplus10)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration locationplus10: ' + str(i))
print('The objective value for the locationplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i)) 


#%%

statistical_properties_locationmin10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 45,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students,
                                                                          number_of_houses, statistical_properties_locationmin10)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration locationmin10: ' + str(i))
print('The objective value for the locationmin10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))  

#%%

statistical_properties_budgetplus10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 330,
                                         "sigma": 100}}

solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students,
                                                                          number_of_houses, statistical_properties_budgetplus10)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration budgetplus10: ' + str(i))
print('The objective value for the budgetplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))  

#%%

statistical_properties_budgetmin10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 270,
                                         "sigma": 100}}

solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
for i in range(number_of_montecarlo_iterations):
    model, solution_i, allocated_i, objVal, pair_quality_allocated_mean, pair_quality_allocated_stdev = run_model(number_of_students,
                                                                          number_of_houses, statistical_properties_budgetmin10)
    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration budgetmin10: ' + str(i))
print('The objective value for the budgetmin10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i)) 

#%%

solutions_base_model = []
allocated_base_model = []
pair_quality_allocated_mean_i = []
pair_quality_allocated_stdev_i = []
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

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration bscplus10: ' + str(i))
    
print('The objective value for the bscplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i)) 

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

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration bscmin10: ' + str(i))
    
print('The objective value for the bscmin10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))  

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

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration genderplus10: ' + str(i))
    
print('The objective value for the genderplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))   

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

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration gendermin10: ' + str(i))
    
print('The objective value for the gendermin10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))   

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

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration nationalityplus10: ' + str(i))
    
print('The objective value for the nationalityplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i)) 

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

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration nationalitymin10: ' + str(i))
    
print('The objective value for the nationalitymin10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i)) 

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
    # #study
    # Student_dataset1.print_property_stats("study", bin_count=4)
    # Student_dataset1.plot_property_histogram("study", bin_count=4)
    Student_dataset1.adjust_property_bin_by_percentage("study", 1, 10, bin_count=4) #towards 3me
    # Student_dataset1.adjust_property_bin_by_percentage("study", 2, 10, bin_count=4) #towards ae
    # Student_dataset1.adjust_property_bin_by_percentage("study", 3, 10, bin_count=4) #towards cs
    # Student_dataset1.adjust_property_bin_by_percentage("study", 4, 10, bin_count=4) #towards io
    # Student_dataset1.plot_property_histogram("study", bin_count=4)
        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration 3meplus10: ' + str(i))
    
print('The objective value for the 3meplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))  

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
    # #study
    # Student_dataset1.print_property_stats("study", bin_count=4)
    # Student_dataset1.plot_property_histogram("study", bin_count=4)
    # Student_dataset1.adjust_property_bin_by_percentage("study", 1, 10, bin_count=4) #towards 3me
    Student_dataset1.adjust_property_bin_by_percentage("study", 2, 10, bin_count=4) #towards ae
    # Student_dataset1.adjust_property_bin_by_percentage("study", 3, 10, bin_count=4) #towards cs
    # Student_dataset1.adjust_property_bin_by_percentage("study", 4, 10, bin_count=4) #towards io
    # Student_dataset1.plot_property_histogram("study", bin_count=4)
        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration aeplus10: ' + str(i))
    
print('The objective value for the aeplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))   

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
    # #study
    # Student_dataset1.print_property_stats("study", bin_count=4)
    # Student_dataset1.plot_property_histogram("study", bin_count=4)
    # Student_dataset1.adjust_property_bin_by_percentage("study", 1, 10, bin_count=4) #towards 3me
    # Student_dataset1.adjust_property_bin_by_percentage("study", 2, 10, bin_count=4) #towards ae
    Student_dataset1.adjust_property_bin_by_percentage("study", 3, 10, bin_count=4) #towards cs
    # Student_dataset1.adjust_property_bin_by_percentage("study", 4, 10, bin_count=4) #towards io
    # Student_dataset1.plot_property_histogram("study", bin_count=4)
        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration csplus10: ' + str(i))
    
print('The objective value for the csplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))   

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
    # #study
    # Student_dataset1.print_property_stats("study", bin_count=4)
    # Student_dataset1.plot_property_histogram("study", bin_count=4)
    # Student_dataset1.adjust_property_bin_by_percentage("study", 1, 10, bin_count=4) #towards 3me
    # Student_dataset1.adjust_property_bin_by_percentage("study", 2, 10, bin_count=4) #towards ae
    # Student_dataset1.adjust_property_bin_by_percentage("study", 3, 10, bin_count=4) #towards cs
    Student_dataset1.adjust_property_bin_by_percentage("study", 4, 10, bin_count=4) #towards io
    # Student_dataset1.plot_property_histogram("study", bin_count=4)
        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration ioplus10: ' + str(i))
    
print('The objective value for the ioplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i)) 

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
    # #preference
    # Student_dataset1.print_property_stats("preference", bin_count=2)
    # Student_dataset1.plot_property_histogram("preference", bin_count=2)
    Student_dataset1.adjust_property_bin_by_percentage("preference", 1, 10, bin_count=2) #towards shared
    # Student_dataset1.plot_property_histogram("preference", bin_count=2)
    
        
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration preferenceplus10: ' + str(i))
    
print('The objective value for the preferenceplus10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))

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
    # #preference
    # Student_dataset1.print_property_stats("preference", bin_count=2)
    # Student_dataset1.plot_property_histogram("preference", bin_count=2)
    Student_dataset1.adjust_property_bin_by_percentage("preference", 1, -10, bin_count=2) #towards shared
    # Student_dataset1.plot_property_histogram("preference", bin_count=2)
    
    model = Model_generator(Student_dataset1, House_dataset1)
    model.output_to_lp()
    model.optimize()

    #print all x_ij:
    solution_i = [] 
    allocated_i = 0
    for v in model.model.getVars():
          solution_i.append([v.varName,v.x])
          if v.x != 0:
              allocated_i += 1 
    #print(solution_i)
    #print(allocated)
    
    pair_quality_allocated = []
    for n in range(len(solution_i)):
        if solution_i[n][1] == 1:
            student_i = solution_i[n][0].split("_")[1]
            house_i = solution_i[n][0].split("_")[2]
            pair_quality_allocated.append(model.pair_quality_dict[student_i][house_i])
    pair_quality_allocated_mean = statistics.mean(pair_quality_allocated)
    pair_quality_allocated_stdev = statistics.stdev(pair_quality_allocated)

    solutions_base_model.append(objVal)
    allocated_base_model.append(allocated_i)
    pair_quality_allocated_mean_i.append(pair_quality_allocated_mean)
    pair_quality_allocated_stdev_i.append(pair_quality_allocated_stdev)
    print_statusline('iteration preferencemin10: ' + str(i))
    
print('The objective value for the preferencemin10 equals:' , statistics.mean(solutions_base_model),
      'The amount of allocated houseplaces equals:' ,statistics.mean(allocated_base_model),
      'The average objective value equals:' ,statistics.mean(solutions_base_model)/number_of_students,
      'The average objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_mean_i),
      'The stdev objective value over allocated equals:' ,statistics.mean(pair_quality_allocated_stdev_i))  










































