if True:
  from datetime import datetime
  import os.path as path
  import pandas as pd
  import numpy as np
  import python.common.common as c


user_file = "data/users.csv"

def read_users() -> pd.DataFrame:
  if path . exists ( user_file ):
    df = pd . read_csv( user_file )
    for c in ["requested","completed"]:
      df[c] = pd.to_datetime( df[c] )
    return df
  else: return pd . DataFrame()

def create_user() -> pd.Series:
  return pd . Series (
    { "email hash" : c.user,
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
     . to_csv( user_file,
               index = False ) )
