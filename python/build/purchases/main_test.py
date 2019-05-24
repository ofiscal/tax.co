import numpy as np
import pandas as pd

import python.build.purchases.main_defs as defs
import python.common.cl_args as cl
import python.build.classes as cla
import python.build.output_io as oio


if True: # initialize log
  test_output_filename = "purchases_main"
  oio.test_clear( test_output_filename )
  def echo( content ):
    oio.test_write( test_output_filename
                  , content )
  echo( ["starting"] )

def test_drop_if_coicop_or_value_invalid():
  echo( ["\ntest_drop_if_coicop_or_value_invalid()"] )
  df = pd.DataFrame( { "coicop"          : [1, 1,      np.nan]
                     , "25-broad-categs" : [1, 1,      np.nan]
                     , "value"           : [1, np.nan, 1     ] } )
  assert ( ( defs.drop_if_coicop_or_value_invalid( df )
           == pd.DataFrame( { "coicop"          : [1]
                            , "25-broad-categs" : [1]
                            , "value"           : [1] } )  )
         . all() . all() )

def test_output():
  echo( ["\ntest_output() "] )
  df = oio.readStage( cl.subsample, 'purchases_1' )
  spec = {
      "where-got" :        { cla.IsNull(), cla.InRange(1,26) }
    , "weight" :           {               cla.InRange( 0, 1e4 ) }
    , "value" :            {               cla.InRange( 0, 1e9 ) }
    , "quantity" :         { cla.IsNull(), cla.InRange( -2, 1e8 ) }
    , "is-purchase" :      { cla.IsNull(), cla.InRange( 0,1 ) }
    , "household-member" : {               cla.InRange( 1, 1e3 ) }
    , "household" :        {               cla.InRange( 1, 1e7 ) }
    , "freq" :             { cla.IsNull(), cla.InRange( 1, 11 ) }
    , "coicop" :           { cla.IsNull(), cla.InRange( 1, 1e8 ) }
    , "25-broad-categs" :  { cla.IsNull(), cla.InRange( 1, 25 ) }
  }
  for k in spec:
    echo( [k] )
    assert cla.properties_cover_num_column( spec[k], df[k] )

  echo( ["Testing that specs cover all column names."] )
  assert set( df.columns ) == set( spec.keys() )

if True: # run the tests
  test_output()
  test_drop_if_coicop_or_value_invalid()
