# TODO ? PTIFALL: All of these do IO, often destructively.
# Maybe I should make them functional and bump the IO
# into the calling code.

if True:
  from datetime import datetime
  import os.path as path
  import pandas as pd
  import numpy as np
  import python.common.common as c


constraints_file = "data/constraints-time-memory.json"
requests_file = "data/requests.csv"

def read_users() -> pd.DataFrame:
  if path . exists ( requests_file ):
    df = pd . read_csv( requests_file )
    for c in ["requested","completed"]:
      df[c] = pd.to_datetime( df[c] )
    return df
  else: return pd . DataFrame()

def create_user() -> pd.Series:
  return pd . Series (
    { "user" : c.user,
      "requested"  : datetime.now(),
      "completed"  : np.nan
    } )

def append_user():
    users = read_users()
    user = create_user()
    ( users
     . append (
         user,
         ignore_index = True )
     . to_csv( requests_file,
               index = False ) )

def uniquify_requests():
    df = ( pd . read_csv( requests_file )
           . sort_values( ["user","requested"],
                          ascending = False )
           . groupby( ["user"] )
           . agg( "first" )
           . reset_index() )
    df . to_csv( requests_file,
                 index = False )

def delete_oldest():
