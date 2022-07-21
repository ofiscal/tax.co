import pandas as pd

import python.build.ss.schedules as sss


pension_contractor_frame = pd.DataFrame (
  { "min_threshold_in_min_wages" : [0    , 1   ],
    "fraction_of_wage"           : [0    , 0.4 ],
    "min_base_in_min_wages"      : [-9e99, 1   ],
    "max_base_in_min_wages"      : [9e99 , 25  ],
    "average_tax_rate"           : [0    , 0.16], } )

pension_contractor_schedule_from_frame = sss.ss_tax_schedule_from_frame (
  df = pension_contractor_frame )

for b in [0,1]: # tax bracket
  for i in [0,2]: # list index
    assert ( pension_contractor_schedule_from_frame             [0][i] ==
             sss.ss_contrib_schedule_for_contractor ["pension"] [0][i] )

  for w in range(25): # wage
    assert ( pension_contractor_schedule_from_frame             [0][1] (w) ==
             sss.ss_contrib_schedule_for_contractor ["pension"] [0][1] (w) )
