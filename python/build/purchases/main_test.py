import numpy as np
import pandas as pd

import python.build.purchases.main_defs as defs
import python.common.cl_args as cl
import python.build.classes as cla
import python.build.output_io as oio


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
  df = pd.DataFrame( { "value"    : [1, thresh+1, thresh+1, 1       ]
                     , "quantity" : [1, 1e-3    , 1       , thresh+1]
                     , "x"        : [1, 2       , 3       , 4       ] } )
  assert ( defs.drop_absurdly_big_expenditures( df )["x"]
           == pd.Series( [1,2] )
         ).all()
  return log

def test_output( df ):
  log = "test_output\n"
  spec = {
      "where-got" :        { cla.IsNull(), cla.InRange(1,26) }
    , "weight" :           {               cla.InRange( 0, 1e4 ) }
    , "value" :            {               cla.InRange( 0, 1e9 ) }
    , "quantity" :         { cla.IsNull(), cla.InRange( -2, 1e8 ) }
    , "is-purchase" :      { cla.IsNull(), cla.InRange( 0,1 ) }
    , "household-member" : {               cla.InRange( 1, 1e3 ) }
    , "household" :        {               cla.InRange( 1, 1e7 ) }
    , "per month" :        { cla.IsNull(), cla.InRange( 1, 11 ) }
    , "coicop" :           { cla.IsNull(), cla.InRange( 1, 1e8 ) }
    , "25-broad-categs" :  { cla.IsNull(), cla.InRange( 1, 25 ) }
  }
  for k in spec:
    log += ("  " + k + "\n")
    assert cla.properties_cover_num_column( spec[k], df[k] )

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
  df = oio.readStage( cl.subsample, 'purchases_1' )
  log += test_output( df )

  oio.test_write( cl.subsample
                , "purchases_main"
                , log )
