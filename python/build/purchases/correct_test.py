if True:
  import numpy as np
  import pandas as pd
  #
  import python.build.purchases.correct_defs as defs
  import python.common.common as com
  import python.build.classes as cla
  import python.build.output_io as oio
  from   python.common.misc import num_purchases_surviving
  from   python.common.util import unique, near


def test_drop_if_coicop_or_value_invalid():
  log = "test_drop_if_coicop_or_value_invalid()"
  df = pd.DataFrame( { "coicop"          : [1, 1,      np.nan]
                     , "25-broad-categs" : [1, 1,      np.nan]
                     , "value"           : [1, np.nan, 1     ] } )
  assert ( ( defs.drop_if_coicop_or_value_invalid( df )
           == pd.DataFrame( { "coicop"          : [1]
                            , "25-broad-categs" : [1]
                            , "value"           : [1] } )  )
         . all() . all() )
  return log

def test_drop_absurdly_big_expenditures():
  log = "test_drop_absurdly_big_expenditures\n"
  thresh = defs.absurdly_big_expenditure_threshold
  df = pd.DataFrame( { "value"    : [1, thresh+1, thresh+1, 1       ],
                       "quantity" : [1, 1e-3    , 1e3     , thresh+1],
                       "x"        : [1, 2       , 3       , 4       ] } )

  assert ( defs.drop_absurdly_big_expenditures( df )
           ["x"] .
           reset_index( drop = True ) .
           equals( pd.Series( [1,4] ) ) )
  return log

def test_output( df ):
  log = "test_output\n"
  assert( unique( df.columns ) )

  assert near(
    len(df),
    num_purchases_surviving / com.subsample,
    tol_frac = 1/20 )

  spec = {
    "where-got" :        cla.InRange(1,26),
    "weight" :           cla.InRange( 0, 1e4 ),
    "value" :            cla.InRange( 0, 1e9 ),
    "quantity" :         cla.InRange( 0, 1e8 ),
    "is-purchase" :      cla.InRange( 0,1 ),
    "household" :        cla.InRange( 1, 1e7 ),
    "per month" :        cla.InRange( 1, 11 ),
    "coicop" :           cla.InRange( 1, 1e8 ),
    "25-broad-categs" :  cla.InRange( 1, 25 )
  }
  for k in spec:
    log += ("  " + k + "\n")
    assert spec[k] . test( df[k] )

  log += "Specs cover all column names."
  assert set( df.columns ) == set( spec.keys() )

  log += "Very few missing quantity values."
  assert ( (1e-5)
           > ( len( df[ pd.isnull( df["quantity"] ) ] ) / len(df) ) )

  log += "Very few negative quantity values."
  assert ( (1e-5)
           > ( len( df[ df["quantity"] <= 0 ] ) / len(df) ) )

  log += "Negative quantity purchases are for very little money."
  assert ( df[ df["quantity"] < 0 ]["value"]
           < 1e4 ).all()

  log += "Very few purchases with a frequency of \"never\"."
  assert ( (1e-5)
           > ( len( df[ df["per month"] > 10 ] ) / len(df) ) )

  log += "Those few frequency=\"never\" purchases are for very little money."
  assert ( df[ df["per month"] > 10 ]["value"]
           < 1e4 ).all()

  return log

if True: # run the tests
  log = "starting\n"

  # unit tests
  log += test_drop_if_coicop_or_value_invalid()
  log += test_drop_absurdly_big_expenditures()

  # integration test
  df = oio.readStage( com.subsample, 'purchases_1' )
  log += test_output( df )

  oio.test_write( com.subsample
                , "purchases_correct"
                , log )

