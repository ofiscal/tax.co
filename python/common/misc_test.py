import numpy as np
import pandas as pd

import python.common.test as t
import python.common.misc as defs
import python.build.output_io as oio


if True: # initialize log
  test_output_filename = "common_util"
  oio.test_clear( test_output_filename )
  def echo( content ):
    oio.test_write( test_output_filename
                  , content )
  echo( ["starting"] )

def test_all_columns_to_numbers():
  assert pd.DataFrame.equals(
    defs.all_columns_to_numbers(
      pd.DataFrame( ["1", 1,  "nan",     "", np.nan ] ) )
    , pd.DataFrame( [1,   1, np.nan, np.nan, np.nan ] ) )

  # will_not_convert is just like the previous data frame,
  # except for the new value "boo"
  will_not_convert = pd.DataFrame(
                ["boo", "1", 1,  "nan",     "", np.nan ] )
  assert pd.DataFrame.equals(
    defs.all_columns_to_numbers( will_not_convert )
    , will_not_convert )

if True: # run tests
  test_all_columns_to_numbers()
