\ Model OO_assignment_model
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  2.760869565217392 x_0_0 + 1.92961281622115 x_0_1 + 2.2415253132707 x_0_2
   + 1.425360062208961 x_0_3 + 3.779863937384433 x_1_0
   + 3.708613711784988 x_1_1 + 3.273153250577193 x_1_2
   + 3.719206847444796 x_1_3 + 3.258951389855916 x_2_0
   + 3.208613711784988 x_2_1 + 2.773153250577193 x_2_2
   + 3.260912347524048 x_2_3 + 2.079863937384433 x_3_0
   + 2.008613711784987 x_3_1 + 1.573153250577193 x_3_2
   + 1.970544645830508 x_3_3 + 2.8 x_4_0 + 2.423174271766256 x_4_1
   + 2.376307921966352 x_4_2 + 2.262464887500142 x_4_3 + 3.5 x_5_0
   + 3.11966870647302 x_5_1 + 3.076307921966352 x_5_2
   + 2.95824820912048 x_5_3 + 3.241709278235807 x_6_0
   + 3.14006183968967 x_6_1 + 2.618779193152921 x_6_2
   + 2.756091399313246 x_6_3 + 1.595778916148904 x_7_0
   + 1.735849238325514 x_7_1 + 1.1 x_7_2 + 1.633757138241885 x_7_3
   + 3.528345222936268 x_8_0 + 3.552930065787786 x_8_1
   + 2.956106382093013 x_8_2 + 3.232425763193547 x_8_3 + 2.3 x_9_0
   + 1.973091077090715 x_9_1 + 1.876307921966352 x_9_2
   + 1.95483820043181 x_9_3 + y_study_ae_0 + y_study_cs_0 + y_study_3me_0
   + y_study_io_0 - 100 y_slack_0 + y_study_ae_1 + y_study_cs_1
   + y_study_3me_1 + y_study_io_1 - 100 y_slack_1 + y_study_ae_2
   + y_study_cs_2 + y_study_3me_2 + y_study_io_2 - 100 y_slack_2
   + y_study_ae_3 + y_study_cs_3 + y_study_3me_3 + y_study_io_3
   - 100 y_slack_3
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
 C_supply_0: x_0_0 + x_1_0 + x_2_0 + x_3_0 + x_4_0 + x_5_0 + x_6_0 + x_7_0
   + x_8_0 + x_9_0 = 6
 C_supply_1: x_0_1 + x_1_1 + x_2_1 + x_3_1 + x_4_1 + x_5_1 + x_6_1 + x_7_1
   + x_8_1 + x_9_1 = 3
 C_supply_2: x_0_2 + x_1_2 + x_2_2 + x_3_2 + x_4_2 + x_5_2 + x_6_2 + x_7_2
   + x_8_2 + x_9_2 = 5
 C_supply_3: x_0_3 + x_1_3 + x_2_3 + x_3_3 + x_4_3 + x_5_3 + x_6_3 + x_7_3
   + x_8_3 + x_9_3 = 4
 C_gs_0: x_0_0 + x_2_0 + x_3_0 + x_4_0 + x_5_0 + x_6_0 + x_8_0 >= 2
 C_gs_1: x_0_1 + x_2_1 + x_3_1 + x_4_1 + x_5_1 + x_6_1 + x_8_1 >= 2
 C_gs_2: x_0_2 + x_2_2 + x_3_2 + x_4_2 + x_5_2 + x_6_2 + x_8_2 >= 2
 C_gs_3: x_0_3 + x_2_3 + x_3_3 + x_4_3 + x_5_3 + x_6_3 + x_8_3 >= 2
 C_fyp: = 0
 C_study_ae_0: x_1_0 + x_2_0 + x_3_0 + 6 y_study_ae_0 >= 6
 C_study_cs_0: x_6_0 + x_8_0 + 6 y_study_cs_0 >= 6
 C_study_3me_0: x_0_0 + x_4_0 + x_5_0 + x_9_0 + 6 y_study_3me_0 >= 6
 C_study_io_0: x_7_0 + 6 y_study_io_0 >= 6
 Study_K_of_N_0: y_study_ae_0 + y_study_cs_0 + y_study_3me_0 + y_study_io_0
   - 100 y_slack_0 <= 1
 C_study_ae_1: x_1_1 + x_2_1 + x_3_1 + 3 y_study_ae_1 >= 3
 C_study_cs_1: x_6_1 + x_8_1 + 3 y_study_cs_1 >= 3
 C_study_3me_1: x_0_1 + x_4_1 + x_5_1 + x_9_1 + 3 y_study_3me_1 >= 3
 C_study_io_1: x_7_1 + 3 y_study_io_1 >= 3
 Study_K_of_N_1: y_study_ae_1 + y_study_cs_1 + y_study_3me_1 + y_study_io_1
   - 100 y_slack_1 <= 1
 C_study_ae_2: x_1_2 + x_2_2 + x_3_2 + 5 y_study_ae_2 >= 5
 C_study_cs_2: x_6_2 + x_8_2 + 5 y_study_cs_2 >= 5
 C_study_3me_2: x_0_2 + x_4_2 + x_5_2 + x_9_2 + 5 y_study_3me_2 >= 5
 C_study_io_2: x_7_2 + 5 y_study_io_2 >= 5
 Study_K_of_N_2: y_study_ae_2 + y_study_cs_2 + y_study_3me_2 + y_study_io_2
   - 100 y_slack_2 <= 1
 C_study_ae_3: x_1_3 + x_2_3 + x_3_3 + 4 y_study_ae_3 >= 4
 C_study_cs_3: x_6_3 + x_8_3 + 4 y_study_cs_3 >= 4
 C_study_3me_3: x_0_3 + x_4_3 + x_5_3 + x_9_3 + 4 y_study_3me_3 >= 4
 C_study_io_3: x_7_3 + 4 y_study_io_3 >= 4
 Study_K_of_N_3: y_study_ae_3 + y_study_cs_3 + y_study_3me_3 + y_study_io_3
   - 100 y_slack_3 <= 1
Bounds
Binaries
 x_0_0 x_0_1 x_0_2 x_0_3 x_1_0 x_1_1 x_1_2 x_1_3 x_2_0 x_2_1 x_2_2 x_2_3
 x_3_0 x_3_1 x_3_2 x_3_3 x_4_0 x_4_1 x_4_2 x_4_3 x_5_0 x_5_1 x_5_2 x_5_3
 x_6_0 x_6_1 x_6_2 x_6_3 x_7_0 x_7_1 x_7_2 x_7_3 x_8_0 x_8_1 x_8_2 x_8_3
 x_9_0 x_9_1 x_9_2 x_9_3 y_study_ae_0 y_study_cs_0 y_study_3me_0
 y_study_io_0 y_slack_0 y_study_ae_1 y_study_cs_1 y_study_3me_1
 y_study_io_1 y_slack_1 y_study_ae_2 y_study_cs_2 y_study_3me_2
 y_study_io_2 y_slack_2 y_study_ae_3 y_study_cs_3 y_study_3me_3
 y_study_io_3 y_slack_3
End
