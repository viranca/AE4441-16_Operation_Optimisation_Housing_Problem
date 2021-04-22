\ Model OO_assignment_model
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  3.698069071222977 x_0_0 + 3.136981269655588 x_0_1
   + 3.636196796922095 x_0_2 + 3.335609867218626 x_0_3
   + 1.073477332510201 x_1_0 + 0.3723550557101931 x_1_1
   + 0.9482044818404427 x_1_2 + 0.9790296558833714 x_1_3
   + 2.728154964513326 x_2_0 + 2.488697430275972 x_2_1 + 2.8 x_2_2
   + 2.520906875653722 x_2_3 + 3.328154964513326 x_3_0
   + 3.127337306628368 x_3_1 + 3.4 x_3_2 + 3.120906875653722 x_3_3
   + 2.968614698553544 x_4_0 + 2.595319550222593 x_4_1
   + 2.909427624967888 x_4_2 + 2.642631043619917 x_4_3
   + 3.521335201117362 x_5_0 + 3.191081217553907 x_5_1
   + 3.547251217814892 x_5_2 + 3.508241600775504 x_5_3
   + 2.335592027940711 x_6_0 + 1.802910602910603 x_6_1
   + 2.30709595420555 x_6_2 + 2.945757023538784 x_6_3
   + 1.307112183736121 x_7_0 + 0.5890806623066168 x_7_1
   + 1.175839278520412 x_7_2 + 1.238028374053536 x_7_3
   + 1.970393263288919 x_8_0 + 1.549847193122329 x_8_1
   + 1.894439733568037 x_8_2 + 1.790420159266175 x_8_3
   + 1.569403624981008 x_9_0 + 1.02660687593423 x_9_1
   + 1.537318242723803 x_9_2 + 2.194741606604084 x_9_3
   + 3.261488297846659 x_10_0 + 2.975048669040861 x_10_1
   + 3.312331717824448 x_10_2 + 3.054240208987056 x_10_3
   + 3.170997968809409 x_11_0 + 2.527219319523966 x_11_1
   + 3.066072856935141 x_11_2 + 2.990534850910733 x_11_3
   + 2.898069071222977 x_12_0 + 2.335373467989408 x_12_1
   + 2.836196796922095 x_12_2 + 2.535609867218626 x_12_3
   + 3.793182378935178 x_13_0 + 3.472531857539277 x_13_1
   + 3.773351298193887 x_13_2 + 3.37596437695325 x_13_3
   + 3.364982921502573 x_14_0 + 3.039165263617615 x_14_1
   + 3.39247311827957 x_14_2 + 3.345234832642969 x_14_3 - 5 Dutch_slack_x_0
   - 5 Dutch_slack_x_1 - 5 Dutch_slack_x_2 - 5 Dutch_slack_x_3
   - 5 Study_slack_x_0 - 5 Study_slack_x_1 - 5 Study_slack_x_2
   - 5 Study_slack_x_3
Subject To
 C_demand_0: x_0_0 + x_0_1 + x_0_2 + x_0_3 <= 1
 C_demand_1: x_1_0 + x_1_1 + x_1_2 + x_1_3 <= 1
 C_demand_2: x_2_0 + x_2_1 + x_2_2 + x_2_3 <= 1
 C_demand_3: x_3_0 + x_3_1 + x_3_2 + x_3_3 <= 1
 C_demand_4: x_4_0 + x_4_1 + x_4_2 + x_4_3 <= 1
 C_demand_5: x_5_0 + x_5_1 + x_5_2 + x_5_3 <= 1
 C_demand_6: x_6_0 + x_6_1 + x_6_2 + x_6_3 <= 1
 C_demand_7: x_7_0 + x_7_1 + x_7_2 + x_7_3 <= 1
 C_demand_8: x_8_0 + x_8_1 + x_8_2 + x_8_3 <= 1
 C_demand_9: x_9_0 + x_9_1 + x_9_2 + x_9_3 <= 1
 C_demand_10: x_10_0 + x_10_1 + x_10_2 + x_10_3 <= 1
 C_demand_11: x_11_0 + x_11_1 + x_11_2 + x_11_3 <= 1
 C_demand_12: x_12_0 + x_12_1 + x_12_2 + x_12_3 <= 1
 C_demand_13: x_13_0 + x_13_1 + x_13_2 + x_13_3 <= 1
 C_demand_14: x_14_0 + x_14_1 + x_14_2 + x_14_3 <= 1
 C_supply_0: x_0_0 + x_1_0 + x_2_0 + x_3_0 + x_4_0 + x_5_0 + x_6_0 + x_7_0
   + x_8_0 + x_9_0 + x_10_0 + x_11_0 + x_12_0 + x_13_0 + x_14_0 = 3
 C_supply_1: x_0_1 + x_1_1 + x_2_1 + x_3_1 + x_4_1 + x_5_1 + x_6_1 + x_7_1
   + x_8_1 + x_9_1 + x_10_1 + x_11_1 + x_12_1 + x_13_1 + x_14_1 = 2
 C_supply_2: x_0_2 + x_1_2 + x_2_2 + x_3_2 + x_4_2 + x_5_2 + x_6_2 + x_7_2
   + x_8_2 + x_9_2 + x_10_2 + x_11_2 + x_12_2 + x_13_2 + x_14_2 = 5
 C_supply_3: x_0_3 + x_1_3 + x_2_3 + x_3_3 + x_4_3 + x_5_3 + x_6_3 + x_7_3
   + x_8_3 + x_9_3 + x_10_3 + x_11_3 + x_12_3 + x_13_3 + x_14_3 = 7
 C_fyp: = 0
 C_gender_split_0: x_1_0 + x_2_0 + x_3_0 + x_7_0 + x_8_0 + x_10_0
   + 1000 Gender_conditional_0 >= 2
 C_gender_split_0: x_1_0 + x_2_0 + x_3_0 + x_7_0 + x_8_0 + x_10_0
   + 1000 Gender_conditional_0 <= 1000
 C_gender_split_1: x_1_1 + x_2_1 + x_3_1 + x_7_1 + x_8_1 + x_10_1
   + 1000 Gender_conditional_1 >= 2
 C_gender_split_1: x_1_1 + x_2_1 + x_3_1 + x_7_1 + x_8_1 + x_10_1
   + 1000 Gender_conditional_1 <= 1000
 C_gender_split_2: x_1_2 + x_2_2 + x_3_2 + x_7_2 + x_8_2 + x_10_2
   + 1000 Gender_conditional_2 >= 2
 C_gender_split_2: x_1_2 + x_2_2 + x_3_2 + x_7_2 + x_8_2 + x_10_2
   + 1000 Gender_conditional_2 <= 1000
 C_gender_split_3: x_1_3 + x_2_3 + x_3_3 + x_7_3 + x_8_3 + x_10_3
   + 1000 Gender_conditional_3 >= 2
 C_gender_split_3: x_1_3 + x_2_3 + x_3_3 + x_7_3 + x_8_3 + x_10_3
   + 1000 Gender_conditional_3 <= 1000
 C_dutch_constraint_0: x_0_0 + x_2_0 + x_4_0 + x_5_0 + x_7_0 + x_8_0
   + x_9_0 + x_14_0 + 5000 Dutch_slack_x_0 >= 3
 C_dutch_constraint_1: x_0_1 + x_2_1 + x_4_1 + x_5_1 + x_7_1 + x_8_1
   + x_9_1 + x_14_1 + 5000 Dutch_slack_x_1 >= 2
 C_dutch_constraint_2: x_0_2 + x_2_2 + x_4_2 + x_5_2 + x_7_2 + x_8_2
   + x_9_2 + x_14_2 + 5000 Dutch_slack_x_2 >= 5
 C_dutch_constraint_3: x_0_3 + x_2_3 + x_4_3 + x_5_3 + x_7_3 + x_8_3
   + x_9_3 + x_14_3 + 5000 Dutch_slack_x_3 >= 7
 C_study_ae_0: x_4_0 + x_8_0 + x_13_0 + 1000 Study_conditional_ae_0 >= 1
 C_study_cs_0: x_2_0 + x_3_0 + x_5_0 + x_10_0 + x_14_0
   + 1000 Study_conditional_cs_0 >= 1
 C_study_3me_0: x_6_0 + x_9_0 + 1000 Study_conditional_3me_0 >= 1
 C_study_io_0: x_0_0 + x_1_0 + x_7_0 + x_11_0 + x_12_0
   + 1000 Study_conditional_io_0 >= 1
 Study_K_of_N_lower_0: Study_conditional_ae_0 + Study_conditional_cs_0
   + Study_conditional_3me_0 + Study_conditional_io_0
   + 5000 Study_slack_x_0 >= 3
 Study_K_of_N_upper_0: Study_conditional_ae_0 + Study_conditional_cs_0
   + Study_conditional_3me_0 + Study_conditional_io_0 <= 3
 C_study_ae_1: x_4_1 + x_8_1 + x_13_1 + 1000 Study_conditional_ae_1 >= 1
 C_study_cs_1: x_2_1 + x_3_1 + x_5_1 + x_10_1 + x_14_1
   + 1000 Study_conditional_cs_1 >= 1
 C_study_3me_1: x_6_1 + x_9_1 + 1000 Study_conditional_3me_1 >= 1
 C_study_io_1: x_0_1 + x_1_1 + x_7_1 + x_11_1 + x_12_1
   + 1000 Study_conditional_io_1 >= 1
 Study_K_of_N_lower_1: Study_conditional_ae_1 + Study_conditional_cs_1
   + Study_conditional_3me_1 + Study_conditional_io_1
   + 5000 Study_slack_x_1 >= 3
 Study_K_of_N_upper_1: Study_conditional_ae_1 + Study_conditional_cs_1
   + Study_conditional_3me_1 + Study_conditional_io_1 <= 3
 C_study_ae_2: x_4_2 + x_8_2 + x_13_2 + 1000 Study_conditional_ae_2 >= 1
 C_study_cs_2: x_2_2 + x_3_2 + x_5_2 + x_10_2 + x_14_2
   + 1000 Study_conditional_cs_2 >= 1
 C_study_3me_2: x_6_2 + x_9_2 + 1000 Study_conditional_3me_2 >= 1
 C_study_io_2: x_0_2 + x_1_2 + x_7_2 + x_11_2 + x_12_2
   + 1000 Study_conditional_io_2 >= 1
 Study_K_of_N_lower_2: Study_conditional_ae_2 + Study_conditional_cs_2
   + Study_conditional_3me_2 + Study_conditional_io_2
   + 5000 Study_slack_x_2 >= 3
 Study_K_of_N_upper_2: Study_conditional_ae_2 + Study_conditional_cs_2
   + Study_conditional_3me_2 + Study_conditional_io_2 <= 3
 C_study_ae_3: x_4_3 + x_8_3 + x_13_3 + 1000 Study_conditional_ae_3 >= 1
 C_study_cs_3: x_2_3 + x_3_3 + x_5_3 + x_10_3 + x_14_3
   + 1000 Study_conditional_cs_3 >= 1
 C_study_3me_3: x_6_3 + x_9_3 + 1000 Study_conditional_3me_3 >= 1
 C_study_io_3: x_0_3 + x_1_3 + x_7_3 + x_11_3 + x_12_3
   + 1000 Study_conditional_io_3 >= 1
 Study_K_of_N_lower_3: Study_conditional_ae_3 + Study_conditional_cs_3
   + Study_conditional_3me_3 + Study_conditional_io_3
   + 5000 Study_slack_x_3 >= 3
 Study_K_of_N_upper_3: Study_conditional_ae_3 + Study_conditional_cs_3
   + Study_conditional_3me_3 + Study_conditional_io_3 <= 3
Bounds
Binaries
 x_0_0 x_0_1 x_0_2 x_0_3 x_1_0 x_1_1 x_1_2 x_1_3 x_2_0 x_2_1 x_2_2 x_2_3
 x_3_0 x_3_1 x_3_2 x_3_3 x_4_0 x_4_1 x_4_2 x_4_3 x_5_0 x_5_1 x_5_2 x_5_3
 x_6_0 x_6_1 x_6_2 x_6_3 x_7_0 x_7_1 x_7_2 x_7_3 x_8_0 x_8_1 x_8_2 x_8_3
 x_9_0 x_9_1 x_9_2 x_9_3 x_10_0 x_10_1 x_10_2 x_10_3 x_11_0 x_11_1 x_11_2
 x_11_3 x_12_0 x_12_1 x_12_2 x_12_3 x_13_0 x_13_1 x_13_2 x_13_3 x_14_0
 x_14_1 x_14_2 x_14_3 Gender_conditional_0 Gender_conditional_1
 Gender_conditional_2 Gender_conditional_3 Dutch_slack_x_0 Dutch_slack_x_1
 Dutch_slack_x_2 Dutch_slack_x_3 Study_conditional_ae_0
 Study_conditional_cs_0 Study_conditional_3me_0 Study_conditional_io_0
 Study_slack_x_0 Study_conditional_ae_1 Study_conditional_cs_1
 Study_conditional_3me_1 Study_conditional_io_1 Study_slack_x_1
 Study_conditional_ae_2 Study_conditional_cs_2 Study_conditional_3me_2
 Study_conditional_io_2 Study_slack_x_2 Study_conditional_ae_3
 Study_conditional_cs_3 Study_conditional_3me_3 Study_conditional_io_3
 Study_slack_x_3
End
