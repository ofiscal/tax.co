import python.common.util as util
import pandas as pd
import numpy as np

import python.build.output_io as oio


def test_util_pad_column_as_int():
  c = pd.Series( [2, "2","2.0",np.nan] )
  assert pd.Series.equals( 
    util.pad_column_as_int ( 4, c )
    , pd.Series( ["0002","0002","0002",np.nan] ) )


if True: # initialize log
  test_output_filename = "common_util"
  oio.test_clear( test_output_filename )
  def echo( content ):
    oio.test_write( test_output_filename
                  , content )
  echo( ["starting"] )


if True: # run tests
  test_util_pad_column_as_int()

