




from House_dataset import House_dataset
from Student_dataset import Student_dataset
from Model_generator import Model_generator



statistical_properties =              {"room_count": {"mu": 5000,
                                                      "sigma": 1},

                                       "rent_per_room": {"mu": 5000,
                                                         "sigma": 100},

                                       "location": {"mu": 5000,
                                                    "sigma": 25}}

Student_dataset1 = Student_dataset(100)
House_dataset1 = House_dataset(15)


model = Model_generator(Student_dataset1, House_dataset1)
model.output_to_lp()
model.optimize()

solution = []   
for v in model.getVars():
     solution.append([v.varName,v.x])
     
#model.printAttr('X')


#%%
# print(model.house_dataset.statistical_properties)

# model.house_dataset.statistical_properties = {"room_count": {"mu": 5000,
#                                                       "sigma": 1},

#                                        "rent_per_room": {"mu": 5000,
#                                                          "sigma": 100},

#                                        "location": {"mu": 5000,
#                                                     "sigma": 25}}



# print(model.house_dataset.statistical_properties)

# Student_dataset2 = Student_dataset(100)
# House_dataset2 = House_dataset(15)

# model = Model_generator(model.student_dataset, model.house_dataset)
# model.output_to_lp()
# model.optimize()

#%%


from House_dataset import House_dataset
from Student_dataset import Student_dataset
from Model_generator import Model_generator


#do this for varying parameters 
complete_solution = []
for MC_i in range(1000):
    model = Model_generator(Student_dataset(100), House_dataset(15))
    model.output_to_lp()
    model.optimize()  
    solution_i = []   
    for v in model.getVars():
        solution.append([v.varName,v.x])
    complete_solution.append(solution_i)
    


#statistical tests on the complete_solution, and between complete_solutions with different input.
























































