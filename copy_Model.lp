\ Model OO_assignment_model
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  2.497099353318423 x_0_0 + 2.233311805477867 x_0_1
   + 2.419750300160138 x_0_2 + 2.011450752697145 x_0_3
   + 1.424117424174276 x_1_0 + 1.380327832009947 x_1_1
   + 1.748381232675115 x_1_2 + 1.317321640400343 x_1_3
   + 2.872280106716211 x_2_0 + 2.850742052955616 x_2_1
   + 3.194373033421564 x_2_2 + 2.804288835036595 x_2_3
   + 2.878917535136605 x_3_0 + 2.679143987480262 x_3_1
   + 2.784252464662303 x_3_2 + 2.481161538365378 x_3_3
   + 2.371662567570947 x_4_0 + 2.229885249689635 x_4_1
   + 2.705486154190517 x_4_2 + 2.093985749924715 x_4_3
   + 3.533667254995388 x_5_0 + 3.48876404494382 x_5_1
   + 3.619286664428677 x_5_2 + 2.831775332344967 x_5_3
   + 0.9861464507992557 x_6_0 + 0.5705308113715715 x_6_1
   + 0.9236098943811784 x_6_2 + 0.2357244709467672 x_6_3
   + 1.816257162165542 x_7_0 + 1.803426432554401 x_7_1
   + 2.123053721758084 x_7_2 + 1.762090646411695 x_7_3
   + 2.481159420289855 x_8_0 + 2.311166376088907 x_8_1
   + 2.660476931182252 x_8_2 + 2.749460619831004 x_8_3
   + 2.263265126077588 x_9_0 + 2.22280701754386 x_9_1
   + 2.348450867070112 x_9_2 + 1.569125026805839 x_9_3
   - 5 Study_slack_x_0 - 5 Study_slack_x_1 - 5 Study_slack_x_2 - 5 Study_slack_x_3

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


 C_supply_0: x_0_0 + x_1_0 + x_2_0 + x_3_0 + x_4_0 + x_5_0 + x_6_0 + x_7_0 + x_8_0 + x_9_0 = 2
 C_supply_1: x_0_1 + x_1_1 + x_2_1 + x_3_1 + x_4_1 + x_5_1 + x_6_1 + x_7_1 + x_8_1 + x_9_1 = 2
 C_supply_2: x_0_2 + x_1_2 + x_2_2 + x_3_2 + x_4_2 + x_5_2 + x_6_2 + x_7_2 + x_8_2 + x_9_2 = 4
 C_supply_3: x_0_3 + x_1_3 + x_2_3 + x_3_3 + x_4_3 + x_5_3 + x_6_3 + x_7_3 + x_8_3 + x_9_3 = 3


 C_study_ae_0: x_0_0 + x_3_0 + x_6_0 + 1000 Study_conditional_ae_0 >= 1
 C_study_cs_0: x_5_0 + x_9_0 + 1000 Study_conditional_cs_0 >= 1
 C_study_3me_0: x_1_0 + x_2_0 + x_4_0 + x_7_0 + 1000 Study_conditional_3me_0 >= 1
 C_study_io_0: x_8_0 + 1000 Study_conditional_io_0 >= 1

 Study_K_of_N_lower_0: Study_conditional_ae_0 + Study_conditional_cs_0 + Study_conditional_3me_0 + Study_conditional_io_0 + 5000 Study_slack_x_0 >= 3
 Study_K_of_N_upper_0: Study_conditional_ae_0 + Study_conditional_cs_0 + Study_conditional_3me_0 + Study_conditional_io_0 <= 3


 C_study_ae_1: x_0_1 + x_3_1 + x_6_1 + 1000 Study_conditional_ae_1 >= 1
 C_study_cs_1: x_5_1 + x_9_1 + 1000 Study_conditional_cs_1 >= 1
 C_study_3me_1: x_1_1 + x_2_1 + x_4_1 + x_7_1 + 1000 Study_conditional_3me_1 >= 1
 C_study_io_1: x_8_1 + 1000 Study_conditional_io_1 >= 1

 Study_K_of_N_lower_1: Study_conditional_ae_1 + Study_conditional_cs_1 + Study_conditional_3me_1 + Study_conditional_io_1 + 5000 Study_slack_x_1 >= 3
 Study_K_of_N_upper_1: Study_conditional_ae_1 + Study_conditional_cs_1 + Study_conditional_3me_1 + Study_conditional_io_1 <= 3


 C_study_ae_2: x_0_2 + x_3_2 + x_6_2 + 1000 Study_conditional_ae_2 >= 1
 C_study_cs_2: x_5_2 + x_9_2 + 1000 Study_conditional_cs_2 >= 1
 C_study_3me_2: x_1_2 + x_2_2 + x_4_2 + x_7_2 + 1000 Study_conditional_3me_2 >= 1
 C_study_io_2: x_8_2 + 1000 Study_conditional_io_2 >= 1

 Study_K_of_N_lower_2: Study_conditional_ae_2 + Study_conditional_cs_2 + Study_conditional_3me_2 + Study_conditional_io_2 + 5000 Study_slack_x_2 >= 3
 Study_K_of_N_upper_2: Study_conditional_ae_2 + Study_conditional_cs_2 + Study_conditional_3me_2 + Study_conditional_io_2 <= 3


 C_study_ae_3: x_0_3 + x_3_3 + x_6_3 + 1000 Study_conditional_ae_3 >= 1
 C_study_cs_3: x_5_3 + x_9_3 + 1000 Study_conditional_cs_3 >= 1
 C_study_3me_3: x_1_3 + x_2_3 + x_4_3 + x_7_3 + 1000 Study_conditional_3me_3 >= 1
 C_study_io_3: x_8_3 + 1000 Study_conditional_io_3 >= 1

 Study_K_of_N_lower_3: Study_conditional_ae_3 + Study_conditional_cs_3 + Study_conditional_3me_3 + Study_conditional_io_3 + 5000 Study_slack_x_3 >= 3
 Study_K_of_N_upper_3: Study_conditional_ae_3 + Study_conditional_cs_3 + Study_conditional_3me_3 + Study_conditional_io_3 <= 3

Bounds
Binaries
 x_0_0 x_0_1 x_0_2 x_0_3 x_1_0 x_1_1 x_1_2 x_1_3 x_2_0 x_2_1 x_2_2 x_2_3
 x_3_0 x_3_1 x_3_2 x_3_3 x_4_0 x_4_1 x_4_2 x_4_3 x_5_0 x_5_1 x_5_2 x_5_3
 x_6_0 x_6_1 x_6_2 x_6_3 x_7_0 x_7_1 x_7_2 x_7_3 x_8_0 x_8_1 x_8_2 x_8_3
 x_9_0 x_9_1 x_9_2 x_9_3

 Study_conditional_ae_0 Study_conditional_cs_0 Study_conditional_3me_0 Study_conditional_io_0 Study_slack_x_0
 Study_conditional_ae_1 Study_conditional_cs_1 Study_conditional_3me_1 Study_conditional_io_1 Study_slack_x_1
 Study_conditional_ae_2 Study_conditional_cs_2 Study_conditional_3me_2 Study_conditional_io_2 Study_slack_x_2
 Study_conditional_ae_3 Study_conditional_cs_3 Study_conditional_3me_3 Study_conditional_io_3 Study_slack_x_3
End
