if True:
  import pandas as pd
  import numpy as np
  #  
  import python.common.common as cl
  import python.common.util as util
  import python.build.output_io as oio


def test_near():
  assert     util.near( 1e4, 1e4 + 5 )
  assert not util.near( 1e4, 1e4 + 15 )
  assert     util.near( 0,   1,      tol_frac = 0,   tol_abs = 2 )
  assert not util.near( 0,   1,      tol_frac = 0,   tol_abs = 1/2 )
  assert     util.near( 20, 21,      tol_frac = 0.1, tol_abs = 0 )
  assert not util.near( 20, 23,      tol_frac = 0.1, tol_abs = 0 )

def test_tuple_by_threshold():
    sched = [(0,"a","b")]
    for income in [-1,0,1,1e11]:
      assert util.tuple_by_threshold( income, sched ) == sched[0]
    sched = [ (0,1,2),
              (10,"whatever","something") ]
    for income in [(-1,0,1,9)]:
      assert util.tuple_by_threshold( income, sched ) == sched[0]
    for income in [(10,11,1e11)]:
      assert util.tuple_by_threshold( income, sched ) == sched[1]

def test_util_pad_column_as_int():
  c = pd.Series( [2, "2","2.0",np.nan] )
  assert pd.Series.equals(
    util.pad_column_as_int ( 4, c )
    , pd.Series( ["0002","0002","0002",np.nan] ) )


if True: # run tests
  log = "starting\n"
  test_near()
  test_util_pad_column_as_int()
  oio.test_write( cl.subsample
                , "common_util"
                , log )
