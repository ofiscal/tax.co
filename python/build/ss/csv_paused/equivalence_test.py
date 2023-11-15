"""
PURPOSE:
  To test the equivalence of the old (code-) and new (csv-based)
  idioms for defining SS tax schedules.

PITFALL:
  Those tax scheduels include functions.
  There is no way to test for equivalence of functions
  without accessing their syntax trees.
  This instead tests them for a reasonable range of input values:
  namely, [ i * min_wage for i in range(30) ].
"""

import datetime
import pandas as pd

import python.build.output_io     as oio
import python.build.ss.schedules  as sss
import python.common.common       as common
from   python.common.misc import min_wage
from   python.common.util import near


#####################################################
##### Test pension_contractor_schedule_from_frame
##### without reading a CSV file.
#####################################################

pension_contractor_frame = pd.DataFrame (
  { "min_threshold_in_min_wages" : [0    , 1   ],
    "fraction_of_wage"           : [0    , 0.4 ],
    "min_base_in_min_wages"      : [-9e99, 1   ],
    "max_base_in_min_wages"      : [9e99 , 25  ],
    "average_tax_rate"           : [0    , 0.16], } )

pension_contractor_schedule_from_frame = sss.ss_tax_schedule_from_frame (
  df = pension_contractor_frame )

for b in [0,1]: # tax bracket
  for i in [0,2]: assert ( near ( # list index
      pension_contractor_schedule_from_frame             [0][i],
      sss.ss_contrib_schedule_for_contractor ["pension"] [0][i] ) )

  for w in range(25): assert ( near ( # wage
      pension_contractor_schedule_from_frame             [0][1] (w),
      sss.ss_contrib_schedule_for_contractor ["pension"] [0][1] (w) ) )


#########################################
##### Test every SS tax-encoding CSV file
#########################################

for (new, old) in \
    [ (sss.ss_contrib_schedule_for_contractor_new,
       sss.ss_contrib_schedule_for_contractor),
      (sss.ss_contrib_schedule_for_employee_new,
       sss.ss_contrib_schedule_for_employee),
     ]:
  for t in [ "pension", "salud", "solidaridad"]: # tax
    for b in range ( len ( old [t] ) ): # tax bracket
      for i in [0,2]: # list index
        assert ( near (
          old [t] [b] [i],
          new [t] [b] [i] ) )

      for w in range(30): # wage
        assert ( near (
          old [t] [b] [1] (w * min_wage),
          new [t] [b] [1] (w * min_wage) ) )

for (new, old) in \
    [ (sss.ss_contribs_by_employer_new,
       sss.ss_contribs_by_employer), ]:
  for t in [ "cajas de compensacion",
             "cesantias + primas",
             "parafiscales",
             "pension",
             "salud", ]:
    for b in range ( len ( old [t] ) ): # tax bracket
      for i in [0,2]: # list index
        assert ( near ( old [t] [b] [i],
                        new [t] [b] [i] ) )

      for w in range(30): # wage
        assert ( near ( old [t] [b] [1] (w * min_wage),
                        new [t] [b] [1] (w * min_wage) ) )

for vs in common . valid_subsamples:
  # PITFALL: Looping over subsample sizes because this program
  # doesn't use any data. If it works, it works for all subsamples.
  oio.test_write ( vs
                   , "build_ss_schedules"
                   , str( datetime.datetime.now() ) )
