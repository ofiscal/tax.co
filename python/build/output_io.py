# utilities for reading and writing to disk

import pandas as pd
import os
import python.common.common as c


def test_folder(subsample):
    return os.path.join(
        "users", c.user,
        "test/recip-" + str(subsample) )
def data_folder(subsample):
    return os.path.join(
        "users", c.user,
        "data/recip-" + str(subsample) )

def test_write( subsample, filename, content ):
  """ This idiom for logging test results is mostly unused.
For some good example code that uses it,
see python/build/purchases/main_test.py. """
  tf = test_folder( subsample )
  if not os.path.exists( tf ):
    os.makedirs( tf )
  with open(
      os.path.join(
          tf,
          filename + ".txt" ),
      'a+' ) as f:
    f.write( "".join( map( str, content ) )
           + "\n" )

def saveStage(subsample,data,name,**kwargs):
  df = data_folder(subsample)
  if not os.path.exists( df ):
    os.makedirs(         df )
  path = os.path.join( df,
                       name + ".csv" )
  data.to_csv( path, index=False, **kwargs )

def saveStage_excel(subsample,data,name,**kwargs):
  df = data_folder(subsample)
  if not os.path.exists( df ):
    os.makedirs(         df )
  path = os.path.join( df,
                       name + ".xlsx" )
  data.to_excel( path, index=False, **kwargs )

def readUserData(subsample,name,**kwargs):
  return pd.read_csv(
      os.path.join(
          data_folder(subsample),
          name + ".csv" ),
      **kwargs )
