import pandas as pd
import numpy as np

import python.common.cl_args as cl
import python.common.util as util
import python.build.output_io as oio


def test_util_pad_column_as_int():
  c = pd.Series( [2, "2","2.0",np.nan] )
  assert pd.Series.equals(
    util.pad_column_as_int ( 4, c )
    , pd.Series( ["0002","0002","0002",np.nan] ) )


if True: # run tests
  log = "starting\n"
  test_util_pad_column_as_int()
  oio.test_write( cl.subsample
                , "common_util"
                , log )
