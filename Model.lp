\ Model OO_assignment_model
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  1.669098079648046 x_0_0 + 1.609913809440317 x_0_1 + 3 x_1_0
   + 3.187267812369415 x_1_1 + 3.205814429509627 x_2_0
   + 3.178149966312774 x_2_1 + 2.359271523178808 x_3_0
   + 2.210310913009954 x_3_1 - 20 Supply_slack_variable_x_0
   - 20 Supply_slack_variable_x_1 - 5 Dutch_slack_variable_x_0
   - 5 Dutch_slack_variable_x_1 - 5 Study_slack_x_0 - 5 Study_slack_x_1
Subject To
 C_demand_0: x_0_0 + x_0_1 <= 1
 C_demand_1: x_1_0 + x_1_1 <= 1
 C_demand_2: x_2_0 + x_2_1 <= 1
 C_demand_3: x_3_0 + x_3_1 <= 1
 C_fyp: = 0
 C_gender_split_min_0: x_0_0 + 1000 Gender_conditional_0 >= 2
 C_gender_split_0_0: x_0_0 - 1000 Gender_conditional_0 <= 1000
 C_gender_split_min_1: x_0_1 + 1000 Gender_conditional_1 >= 2
 C_gender_split_0_1: x_0_1 - 1000 Gender_conditional_1 <= 1000
 C_supply_lower_0: x_0_0 + x_1_0 + x_2_0 + x_3_0
   + 20000 Supply_slack_variable_x_0 >= 5
 C_supply_upper_0: x_0_0 + x_1_0 + x_2_0 + x_3_0 <= 5
 C_supply_lower_1: x_0_1 + x_1_1 + x_2_1 + x_3_1
   + 20000 Supply_slack_variable_x_1 >= 7
 C_supply_upper_1: x_0_1 + x_1_1 + x_2_1 + x_3_1 <= 7
 C_dutch_constraint_min_0: x_0_0 + x_2_0 + x_3_0 + 5 Dutch_conditional_0
   >= 5
 C_dutch_constraint__0_0: x_0_0 + x_2_0 + x_3_0
   - 5 Dutch_slack_variable_x_0 + 5 Dutch_conditional_0 <= 5
 C_dutch_constraint_min_1: x_0_1 + x_2_1 + x_3_1 + 7 Dutch_conditional_1
   >= 7
 C_dutch_constraint__0_1: x_0_1 + x_2_1 + x_3_1
   - 7 Dutch_slack_variable_x_1 + 7 Dutch_conditional_1 <= 7
 C_study_ae_0: x_0_0 - 1000 Study_conditional_ae_0 <= 0
 C_study_cs_0: x_2_0 - 1000 Study_conditional_cs_0 <= 0
 C_study_3me_0: x_1_0 + x_3_0 - 1000 Study_conditional_3me_0 <= 0
 C_study_io_0: - 1000 Study_conditional_io_0 <= 0
 C_study_K_of_N_lower_0: Study_conditional_ae_0 + Study_conditional_cs_0
   + Study_conditional_3me_0 + Study_conditional_io_0
   - 5000 Study_slack_x_0 <= 1
 C_study_ae_1: x_0_1 - 1000 Study_conditional_ae_1 <= 0
 C_study_cs_1: x_2_1 - 1000 Study_conditional_cs_1 <= 0
 C_study_3me_1: x_1_1 + x_3_1 - 1000 Study_conditional_3me_1 <= 0
 C_study_io_1: - 1000 Study_conditional_io_1 <= 0
 C_study_K_of_N_lower_1: Study_conditional_ae_1 + Study_conditional_cs_1
   + Study_conditional_3me_1 + Study_conditional_io_1
   - 5000 Study_slack_x_1 <= 1
Bounds
Binaries
 x_0_0 x_0_1 x_1_0 x_1_1 x_2_0 x_2_1 x_3_0 x_3_1 Gender_conditional_0
 Gender_conditional_1 Supply_slack_variable_x_0 Supply_slack_variable_x_1
 Dutch_slack_variable_x_0 Dutch_conditional_0 Dutch_slack_variable_x_1
 Dutch_conditional_1 Study_conditional_ae_0 Study_conditional_cs_0
 Study_conditional_3me_0 Study_conditional_io_0 Study_slack_x_0
 Study_conditional_ae_1 Study_conditional_cs_1 Study_conditional_3me_1
 Study_conditional_io_1 Study_slack_x_1
End
