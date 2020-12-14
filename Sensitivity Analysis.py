
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

"""
=============================================================================
Set inputs and statistical properties for the base model:
=============================================================================
"""

number_of_students = 100
number_of_houses = 15
number_of_montecarlo_iterations = 100


statistical_properties_base = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}




"""
=============================================================================
define the function that runs the model, and run the base model:
=============================================================================
"""

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



solutions_base_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_base_model.append(run_model(number_of_students, number_of_houses, statistical_properties_base))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration base model: ' + str(i))
print('The objective value for the base model equals:' , statistics.mean(solutions_base_model))    


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

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_model.append(run_model(number_of_students, number_of_houses, statistical_properties_roomcountplus10))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration roomcountplus10: ' + str(i))
print('The objective value for the roomcountplus10 model equals:' , statistics.mean(solutions_model))  


#%%

statistical_properties_roomcountmin10 = {"room_count": {"mu": 2.7,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_model.append(run_model(number_of_students, number_of_houses, statistical_properties_roomcountmin10))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration roomcountmin10: ' + str(i))
print('The objective value for the roomcountmin10 model equals:' , statistics.mean(solutions_model))  

#%%

statistical_properties_rentplus10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 660,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_model.append(run_model(number_of_students, number_of_houses, statistical_properties_rentplus10))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration rentplus10: ' + str(i))
print('The objective value for the rentplus10 model equals:' , statistics.mean(solutions_model))  

#%%

statistical_properties_rentmin10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 540,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_model.append(run_model(number_of_students, number_of_houses, statistical_properties_rentmin10))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration rentmin10: ' + str(i))
print('The objective value for the rentmin10 model equals:' , statistics.mean(solutions_model))  

#%%

statistical_properties_locationplus10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 55,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_model.append(run_model(number_of_students, number_of_houses, statistical_properties_locationplus10))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration locationplus10: ' + str(i))
print('The objective value for the locationplus10 model equals:' , statistics.mean(solutions_model))  

#%%

statistical_properties_locationmin10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 45,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 300,
                                         "sigma": 100}}

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_model.append(run_model(number_of_students, number_of_houses, statistical_properties_locationmin10))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration locationmin10: ' + str(i))
print('The objective value for the locationmin10 model equals:' , statistics.mean(solutions_model))  

#%%

statistical_properties_budgetplus10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 330,
                                         "sigma": 100}}

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_model.append(run_model(number_of_students, number_of_houses, statistical_properties_budgetplus10))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration budgetplus10: ' + str(i))
print('The objective value for the budgetplus10 model equals:' , statistics.mean(solutions_model))  

##statistical tests on the complete_solution, and between complete_solutions with different input.

#%%

statistical_properties_budgetmin10 = {"room_count": {"mu": 3,
                                        "sigma": 1},

                          "rent_per_room": {"mu": 600,
                                            "sigma": 100},

                          "location": {"mu": 50,
                                       "sigma": 25},
                         
                          "budget_min": {"mu": 270,
                                         "sigma": 100}}

solutions_model = []
for i in range(number_of_montecarlo_iterations):
    solutions_model.append(run_model(number_of_students, number_of_houses, statistical_properties_budgetmin10))
    #print('\x1b[2K' , "iteration {}".format(i) +'\r',  end ='')
    print_statusline('iteration budgetmin10: ' + str(i))
print('The objective value for the budgetmin10 model equals:' , statistics.mean(solutions_model))  


#%%
























































