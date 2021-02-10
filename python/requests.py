 # TODO ? PTIFALL: All of these do IO, often destructively.
# Maybe I should make them functional and bump the IO
# into the calling code.

if True:
  from   datetime import datetime, timedelta
  import json
  import numpy as np
  import os
  import os.path as path
  import pandas as pd
  import subprocess
  from   typing import Callable, Dict
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

def initialize_requests():
  """If the file already exists, this does nothing."""
  if not path . exists ( requests_file ):
       empty_requests () . to_csv ( requests_file,
                                    index = False )

def read_requests() -> pd.DataFrame:
  if path . exists ( requests_file ):
    return format_times (
      pd . read_csv ( requests_file ) )
  else: return empty_requests ()

def gb_used () -> int:
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
    return int( reading ) / 1e6 # divide because `du` gives kb, not gb


#### #### #### #### ####
#### Pure functions ####
#### #### #### #### ####

def memory_permits_another_run ( gb_used : float,
                                 constraints : Dict[ str, str ]
                               ) -> bool:
    gb_unused = constraints["max_gb"] - gb_used
    return gb_unused > constraints["max_user_gb"]

def empty_requests () -> pd.DataFrame:
    return pd.DataFrame(
        columns = ["user","requested","completed"] )

def this_request () -> pd.Series:
  return pd . Series (
    { "user"      : c.user,
      "requested" : datetime.now(),
      "completed" : np.nan
    } )

# Arguably this is too simple to define,
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
    return ( canonicalize_requests( requests ) ) [1:]

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
    return format_times (
        uniquify_requests ( requests )
        . sort_values ( "requested",
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
    return not ( requests [ "completed" ]
                 . isnull()
                 . all () )

def format_times ( requests : pd.DataFrame
                 ) -> pd.DataFrame:
    for c in ["requested","completed"]:
      requests [c] = pd.to_datetime( requests [c] )
    return requests
