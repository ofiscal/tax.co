if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.common as cl
  import python.common.util as util
  import python.build.output_io as oio

def test_noisyQuantile ():
  # Half of this series is exactly zero,
  # so the bin sizes if we used ordinary quantiles would be uneven.
  s = ( pd.concat ( [ pd.Series ( [0] * 500 ),
                      pd.Series ( np.random.rand ( 500 ) ) ] )
        . reset_index ( drop = True ) )

  # n is the series of quantiles (specifically deciles)
  # corresponding to s, labeled from 0 to 9.
  n = ( # This definition won't even work without noise.
    util.noisyQuantile ( n_quantiles = 10,
                         noise_min = 0,
                         noise_max= 0.001,
                         in_col = s )
    . astype ( int ) )

  # The mean of n should be very close to 4.5 = 0 + 9 / 2.
  # The bounds below are wider than would be necessary if I didn't mind
  # the occasional false alarm because randomness put the mean outside
  # where it ought to be.
  assert 4.3 < n.mean()
  assert 4.7 > n.mean()

def test_fuzz_peso_values ():
  df = pd.DataFrame (
    {"s" : [float ( 10**i) for i in range(0,15) ] } )
  df["s+r"] = util.fuzz_peso_values ( df["s"] )
  df["max difference"] = df["s"] . apply (
    lambda x : max ( x * 1e-5, 1 ) )
  assert ( ( ( df["s"] - df["s+r"] ) . abs()
             < df["max difference"] )
           . all () )

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
  for income in [-1,0,1,9]:
    assert util.tuple_by_threshold( income, sched ) == sched[0]
  for income in [10,11,1e11]:
    assert util.tuple_by_threshold( income, sched ) == sched[1]

def test_util_pad_column_as_int():
  c = pd.Series( [2, "2","2.0",np.nan] )
  assert pd.Series.equals(
    util.pad_column_as_int ( 4, c )
    , pd.Series( ["0002","0002","0002",np.nan] ) )


if True: # run tests
  log = "starting\n"
  test_noisyQuantile ()
  test_fuzz_peso_values ()
  test_near ()
  test_tuple_by_threshold ()
  test_util_pad_column_as_int ()
  oio.test_write( cl.subsample
                , "common_util"
                , log )
