 # TODO ? PTIFALL: All of these do IO, often destructively.
# Maybe I should make them functional and bump the IO
# into the calling code.

if True:
  from datetime import datetime, timedelta
  from typing import Callable, Dict
  import json
  import os
  import os.path as path
  import subprocess
  import numpy as np
  import pandas as pd
  #
  import python.common.common as c


users_folder = "users/"
constraints_file = "data/constraints-time-memory.json"
requests_file = "data/requests.csv"


#### #### #### #### #### #### #### ####
#### IO (functions and actions)    ####
#### #### #### #### #### #### #### ####

with open( constraints_file ) as f:
    constraints = json.load( f )

def mutate ( target : str,
             f : Callable [ [ pd.DataFrame ], pd.DataFrame ]
           ):
    df = pd . read_csv ( target )
    f ( df ) . to_csv ( target,
                        index = False )

def read_users() -> pd.DataFrame:
  if path . exists ( requests_file ):
    df = pd . read_csv( requests_file )
    for c in ["requested","completed"]:
      df[c] = pd.to_datetime( df[c] )
    return df
  else: return pd.DataFrame()

def memory_permits_another_run ( constraints : Dict[ str, str ]
                               ) -> bool:
    gb_used = kb_used() / 2e6
    gb_avail = constraints["max_gb"] - gb_used
    return gb_avail > constraints["max_user_gb"]

def kb_used () -> int:
    s = str ( subprocess.Popen( "du -s " + users_folder,
                                shell=True,
                                stdout=subprocess.PIPE)
              . stdout . read () )
    reading = ""
    for i in range( len( s ) ):
        # Incredibly, itertools.takewhile is so unfriendly that
        # it was easier to do this by hand.
        if s [i] . isnumeric ():
            reading = reading + s[i]
        if s [i] . isspace(): break
    return int( reading )


#### #### #### #### ####
#### Pure functions ####
#### #### #### #### ####

def this_request () -> pd.Series:
  return pd . Series (
    { "user"      : c.user,
      "requested" : datetime.now(),
      "completed" : np.nan
    } )

# todo ? maybe this should be inlined,
# but then I'd have to remember the ignore_index option.
def append_request ( requests : pd.DataFrame,
                     request  : pd.Series
                   ) -> pd.DataFrame:
    return ( requests
             . append ( request,
                        ignore_index = True ) )

# PITFALL: This doesn't verify that the oldest has been executed.
# Upstream it should only be called if memory does not permit another run.
# (If memory does not permit another run,
# then at least the oldest request has been executed.)
def delete_oldest ( requests : pd.DataFrame
                  ) -> pd.DataFrame:
    return canonicalize_requests( requests ) [1:]

def at_least_one_is_old ( requests : pd.DataFrame,
                          constraints : Dict[ str, str ]
                        ) -> bool:
    requests = canonicalize_requests( requests )
    now = datetime.now()
    oldest = requests . iloc[0] ["requested"]
    min_survival_time = (
        timedelta ( hours = 1 )
        * ( constraints[ "min_survival_minutes" ] / 60 ) )
    return (now - oldest) > min_survival_time

def canonicalize_requests ( requests : pd.DataFrame
                          ) -> pd.DataFrame:
    """ Calling this everywhere would be wasteful in big data,
    but it's negligible for the request data,
    and safer than assuming upstream functions have already done it."""
    return ( uniquify_requests( requests )
             . sort_values( "requested",
                            ascending = True ) )

def uniquify_requests ( requests : pd.DataFrame
                      ) -> pd.DataFrame:
    return ( requests
             . sort_values( ["user","requested"],
                            ascending = True )
             . groupby( ["user"] )
             . agg( "first" )
               # User keeps their place in line after changing the request.
               # (This database does not know the content of the request,
               # just the time and the user.)
             . reset_index() )

def unexecuted_requests_exist ( requests : pd.DataFrame
                              ) -> bool:
    return requests [ "completed" ] . isnull()
