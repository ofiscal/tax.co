import numpy as np
import pandas as pd

import python.common.test as t
import python.common.misc as defs


def test_all_columns_to_numbers():
  t.afe( defs.all_columns_to_numbers(
         pd.DataFrame( ["1", 1,  "nan",     "", np.nan ] ) )
       , pd.DataFrame( [1,   1, np.nan, np.nan, np.nan ] ) )

  # will_not_convert is just like the previous data frame,
  # except for the new value "boo"
  will_not_convert = pd.DataFrame(
                ["boo", "1", 1,  "nan",     "", np.nan ] )
  t.afe( defs.all_columns_to_numbers( will_not_convert )
       , will_not_convert )

if True: # run tests
  test_all_columns_to_numbers()
