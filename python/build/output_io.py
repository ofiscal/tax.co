# utilities for reading and writing to disk

import pandas as pd
import os

import python.common.common as c


def test_folder(subsample):
    return os.path.join(
        "users", c.user,
        "test/recip-" + str(subsample) )

def get_user_data_folder ( subsample : int) -> str:
  return os.path.join(
    "users",
    c.user,
    "data/recip-" + str(subsample) )

def get_baseline_data_folder ( subsample : int ) -> str:
  return os.path.join(
    "users",
    c.user_hash_from_email ( "baseline" ),
    "data/recip-" + str(subsample) )

def get_common_output_folder(subsample):
  """Data created by the (second) Makefile shared by all users."""
  return os.path.join (
    "output",
    "recip-" + str(subsample) )

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

def saveUserData ( subsample, data, name, **kwargs):
  df = get_user_data_folder(subsample)
  if not os.path.exists( df ):
    os.makedirs(         df )
  path = os.path.join( df,
                       name + ".csv" )
  data.to_csv( path, index=False, **kwargs )

def saveCommonOutput ( subsample, data, name, **kwargs):
  df = get_common_output_folder ( subsample )
  if not os.path.exists( df ):
    os.makedirs(         df )
  path = os.path.join( df,
                       name + ".csv" )
  data.to_csv ( path, index=False, **kwargs )

def saveUserData_excel(subsample,data,name,**kwargs):
  df = get_user_data_folder(subsample)
  if not os.path.exists( df ):
    os.makedirs(         df )
  path = os.path.join( df,
                       name + ".xlsx" )
  data.to_excel( path, index=False, **kwargs )

def readUserData (subsample,name,**kwargs) -> pd.DataFrame():
  return pd.read_csv(
    os.path.join(
      get_user_data_folder ( subsample ),
      name + ".csv" ),
    **kwargs )

def readBaselineData (subsample,name,**kwargs) -> pd.DataFrame():
  return pd.read_csv(
    os.path.join(
      get_baseline_data_folder ( subsample ),
      name + ".csv" ),
    **kwargs )

def readCommonOutput (subsample,name,**kwargs):
  """Read a file from the output of the (second) Makefile, not specific to any user."""
  return pd.read_csv(
    os.path.join(
      get_common_output_folder ( subsample ),
      name + ".csv" ),
    **kwargs )
