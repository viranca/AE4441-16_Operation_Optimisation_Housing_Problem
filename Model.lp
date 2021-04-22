\ Model OO_assignment_model
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  3.0569183905671 x_0_0 + 2.920963557326645 x_0_1 + 2.139047619047619 x_0_2
   + 2.923691894134511 x_0_3 + 1.982488679452561 x_1_0
   + 1.781235138521011 x_1_1 + 1.541181740095551 x_1_2
   + 1.647922208517707 x_1_3 + 2.693275343213729 x_2_0
   + 2.459233249946885 x_2_1 + 2.22052364464992 x_2_2
   + 2.346077216871016 x_2_3 + 2.378650202560192 x_3_0
   + 2.246704200397258 x_3_1 + 2.003810329071445 x_3_2
   + 2.070784176888658 x_3_3 + 1.514112611076492 x_4_0
   + 1.354568471854344 x_4_1 + 1.112805671719482 x_4_2
   + 1.195614516210015 x_4_3 + 2.953281345197771 x_5_0
   + 2.809549984023309 x_5_1 + 2.027952755905511 x_5_2
   + 2.817058973249622 x_5_3 + 1.94374257500593 x_6_0
   + 1.470224236848582 x_6_1 + 1.106885850564031 x_6_2
   + 1.18073628869435 x_6_3 + 2.606516014149048 x_7_0
   + 2.635478645645413 x_7_1 + 3.316928446771379 x_7_2
   + 2.830883321244864 x_7_3 + 1.21873241903561 x_8_0
   + 1.264698121728433 x_8_1 + 1.945939806927882 x_8_2
   + 1.456981058430126 x_8_3 + 2.52060604572395 x_9_0
   + 2.327932638798097 x_9_1 + 1.548341232227488 x_9_2
   + 2.365528951232232 x_9_3 + 2.428237287570818 x_10_0
   + 1.986514963665625 x_10_1 + 1.621873462042871 x_10_2
   + 1.677480285438346 x_10_3 + 3.622924904078235 x_11_0
   + 3.493842705288973 x_11_1 + 2.711645101663586 x_11_2
   + 3.492346061901433 x_11_3 + 2.210333468904377 x_12_0
   + 2.212053105251575 x_12_1 + 2.894619422572179 x_12_2
   + 2.424205523770596 x_12_3 + 2.595578600413751 x_13_0
   + 2.27844539752035 x_13_1 + 1.503954802259887 x_13_2
   + 2.392553879606666 x_13_3 + 2.617766235460731 x_14_0
   + 2.564957361784726 x_14_1 + 3.249758454106281 x_14_2
   + 2.810631405318011 x_14_3 - 5 Dutch_slack_x_0 - 5 Dutch_slack_x_1
   - 5 Dutch_slack_x_2 - 5 Dutch_slack_x_3 - 5 Study_slack_x_0
   - 5 Study_slack_x_1 - 5 Study_slack_x_2 - 5 Study_slack_x_3
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
   + x_8_0 + x_9_0 + x_10_0 + x_11_0 + x_12_0 + x_13_0 + x_14_0 = 4
 C_supply_1: x_0_1 + x_1_1 + x_2_1 + x_3_1 + x_4_1 + x_5_1 + x_6_1 + x_7_1
   + x_8_1 + x_9_1 + x_10_1 + x_11_1 + x_12_1 + x_13_1 + x_14_1 = 2
 C_supply_2: x_0_2 + x_1_2 + x_2_2 + x_3_2 + x_4_2 + x_5_2 + x_6_2 + x_7_2
   + x_8_2 + x_9_2 + x_10_2 + x_11_2 + x_12_2 + x_13_2 + x_14_2 = 2
 C_supply_3: x_0_3 + x_1_3 + x_2_3 + x_3_3 + x_4_3 + x_5_3 + x_6_3 + x_7_3
   + x_8_3 + x_9_3 + x_10_3 + x_11_3 + x_12_3 + x_13_3 + x_14_3 = 4
 C_fyp: x_0_0 + x_0_1 + x_0_2 + x_0_3 = 1
 C_gender_split_0: x_1_0 + x_3_0 + x_5_0 + x_6_0 + x_7_0 + x_9_0 + x_11_0
   + 1000 Gender_conditional_0 >= 2
 C_gender_split_0: x_1_0 + x_3_0 + x_5_0 + x_6_0 + x_7_0 + x_9_0 + x_11_0
   + 1000 Gender_conditional_0 <= 1000
 C_gender_split_1: x_1_1 + x_3_1 + x_5_1 + x_6_1 + x_7_1 + x_9_1 + x_11_1
   + 1000 Gender_conditional_1 >= 2
 C_gender_split_1: x_1_1 + x_3_1 + x_5_1 + x_6_1 + x_7_1 + x_9_1 + x_11_1
   + 1000 Gender_conditional_1 <= 1000
 C_gender_split_2: x_1_2 + x_3_2 + x_5_2 + x_6_2 + x_7_2 + x_9_2 + x_11_2
   + 1000 Gender_conditional_2 >= 2
 C_gender_split_2: x_1_2 + x_3_2 + x_5_2 + x_6_2 + x_7_2 + x_9_2 + x_11_2
   + 1000 Gender_conditional_2 <= 1000
 C_gender_split_3: x_1_3 + x_3_3 + x_5_3 + x_6_3 + x_7_3 + x_9_3 + x_11_3
   + 1000 Gender_conditional_3 >= 2
 C_gender_split_3: x_1_3 + x_3_3 + x_5_3 + x_6_3 + x_7_3 + x_9_3 + x_11_3
   + 1000 Gender_conditional_3 <= 1000
 C_dutch_constraint_0: x_1_0 + x_2_0 + x_3_0 + x_4_0 + x_5_0 + x_6_0
   + x_7_0 + x_8_0 + x_11_0 + x_13_0 + 5000 Dutch_slack_x_0 >= 4
 C_dutch_constraint_1: x_1_1 + x_2_1 + x_3_1 + x_4_1 + x_5_1 + x_6_1
   + x_7_1 + x_8_1 + x_11_1 + x_13_1 + 5000 Dutch_slack_x_1 >= 2
 C_dutch_constraint_2: x_1_2 + x_2_2 + x_3_2 + x_4_2 + x_5_2 + x_6_2
   + x_7_2 + x_8_2 + x_11_2 + x_13_2 + 5000 Dutch_slack_x_2 >= 2
 C_dutch_constraint_3: x_1_3 + x_2_3 + x_3_3 + x_4_3 + x_5_3 + x_6_3
   + x_7_3 + x_8_3 + x_11_3 + x_13_3 + 5000 Dutch_slack_x_3 >= 4
 C_study_ae_0: x_6_0 + x_10_0 + 1000 Study_conditional_ae_0 >= 1
 C_study_cs_0: x_0_0 + x_5_0 + x_9_0 + x_11_0 + x_13_0
   + 1000 Study_conditional_cs_0 >= 1
 C_study_3me_0: x_1_0 + x_2_0 + x_3_0 + x_4_0
   + 1000 Study_conditional_3me_0 >= 1
 C_study_io_0: x_7_0 + x_8_0 + x_12_0 + x_14_0
   + 1000 Study_conditional_io_0 >= 1
 Study_K_of_N_lower_0: Study_conditional_ae_0 + Study_conditional_cs_0
   + Study_conditional_3me_0 + Study_conditional_io_0
   + 5000 Study_slack_x_0 >= 3
 Study_K_of_N_upper_0: Study_conditional_ae_0 + Study_conditional_cs_0
   + Study_conditional_3me_0 + Study_conditional_io_0 <= 3
 C_study_ae_1: x_6_1 + x_10_1 + 1000 Study_conditional_ae_1 >= 1
 C_study_cs_1: x_0_1 + x_5_1 + x_9_1 + x_11_1 + x_13_1
   + 1000 Study_conditional_cs_1 >= 1
 C_study_3me_1: x_1_1 + x_2_1 + x_3_1 + x_4_1
   + 1000 Study_conditional_3me_1 >= 1
 C_study_io_1: x_7_1 + x_8_1 + x_12_1 + x_14_1
   + 1000 Study_conditional_io_1 >= 1
 Study_K_of_N_lower_1: Study_conditional_ae_1 + Study_conditional_cs_1
   + Study_conditional_3me_1 + Study_conditional_io_1
   + 5000 Study_slack_x_1 >= 3
 Study_K_of_N_upper_1: Study_conditional_ae_1 + Study_conditional_cs_1
   + Study_conditional_3me_1 + Study_conditional_io_1 <= 3
 C_study_ae_2: x_6_2 + x_10_2 + 1000 Study_conditional_ae_2 >= 1
 C_study_cs_2: x_0_2 + x_5_2 + x_9_2 + x_11_2 + x_13_2
   + 1000 Study_conditional_cs_2 >= 1
 C_study_3me_2: x_1_2 + x_2_2 + x_3_2 + x_4_2
   + 1000 Study_conditional_3me_2 >= 1
 C_study_io_2: x_7_2 + x_8_2 + x_12_2 + x_14_2
   + 1000 Study_conditional_io_2 >= 1
 Study_K_of_N_lower_2: Study_conditional_ae_2 + Study_conditional_cs_2
   + Study_conditional_3me_2 + Study_conditional_io_2
   + 5000 Study_slack_x_2 >= 3
 Study_K_of_N_upper_2: Study_conditional_ae_2 + Study_conditional_cs_2
   + Study_conditional_3me_2 + Study_conditional_io_2 <= 3
 C_study_ae_3: x_6_3 + x_10_3 + 1000 Study_conditional_ae_3 >= 1
 C_study_cs_3: x_0_3 + x_5_3 + x_9_3 + x_11_3 + x_13_3
   + 1000 Study_conditional_cs_3 >= 1
 C_study_3me_3: x_1_3 + x_2_3 + x_3_3 + x_4_3
   + 1000 Study_conditional_3me_3 >= 1
 C_study_io_3: x_7_3 + x_8_3 + x_12_3 + x_14_3
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
