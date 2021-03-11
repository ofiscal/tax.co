 # TODO ? PTIFALL: All of these do IO, often destructively.
# Maybe I should make them functional and bump the IO
# into the calling code.

if True:
  from   datetime import datetime, timedelta
  import json
  import numpy as np
  import os
  import pandas as pd
  import subprocess
  from   typing import Callable, Dict
  #
  import python.common.common as c


#### #### #### #### #### #### #### ####
#### IO (functions and actions)    ####
#### #### #### #### #### #### #### ####

def mutate ( filename : str,
             f : Callable [ [ pd.DataFrame ], pd.DataFrame ]
           ):
    df = pd . read_csv ( filename )
    f ( df ) . to_csv ( filename,
                        index = False )

def initialize_requests ( requests_file_path : str ):
  """If the file already exists, this does nothing."""
  if not os . path . exists ( requests_file_path ):
       ( empty_requests ()
         . to_csv ( requests_file_path,
                    index = False ) )

def read_requests ( requests_file_path : str ) -> pd.DataFrame:
  if os . path . exists ( requests_file_path ):
    return format_times (
      pd . read_csv ( requests_file_path ) )
  else: return empty_requests ()

def gb_used ( users_folder ) -> int:
    s = str ( subprocess . Popen( "du -s " + users_folder,
                                  shell = True,
                                  stdout = subprocess . PIPE )
              . stdout . read () )
    reading = ""
    for i in range( len( s ) ):
        # itertools.takewhile is so unfriendly that
        # it was easier to do this by hand.
        if s [i] . isnumeric ():
            reading = reading + s[i]
        if s [i] . isspace(): break
    return int( reading ) / 1e6 # divide because `du` gives kb, not gb

# This isn't actually necessary,
# since delete_oldest_request() isn't.
#
# def delete_oldest ( requests_file : str,
#                     users_folder : str ):
#     # TODO: These changes to reqs could be clobbered --
#     # by another instance of the same cron job,
#     # or by a user submitting a new request. Need a mem lock.
#     reqs = lib . read_requests ( requests_file )
#     delete_oldest_user_folder ( reqs, users_folder )
#     reqs = delete_oldest_request ( reqs )
#     reqs . to_csv ( requests_file, index = False )

def delete_oldest_user_folder ( requests : pd.DataFrame,
                                users_folder : str ):
    if True: # Verify that users_folder looks plausible,
             # to be sure it can't delete anything too important.
      (base, last) = os . path . split ( users_folder )
      if last != "users":
        raise Exception ( users_folder + " does not end in `/users`" )
      if base . count ("/") != 4:
        raise Exception ( users_folder + " is not four folders below /." )
    requests = canonicalize_requests( requests )
    oldest_user = requests . iloc[0] ["user"]
    os . system( "rm -rf " + users_folder )

def this_request () -> pd.Series:
  # PITFALL: Looks pure, but in fact through the python.common lib
  # it executes IO, reading the user's config file.
  return pd . Series (
    { "user"      : c . user,
      "requested" : datetime . now (),
      "completed" : np . nan
    } )


#### #### #### #### ####
#### Pure functions ####
#### #### #### #### ####

def memory_permits_another_run (
        gb_used : float,
                                 constraints : Dict[ str, str ]
                               ) -> bool:
    gb_unused = constraints["max_gb"] - gb_used
    return gb_unused > constraints["max_user_gb"]

def empty_requests () -> pd.DataFrame:
    return pd.DataFrame (
        columns = ["user","requested","completed"] )

# Arguably this is too simple to be worth defining,
# but if I didn't, I'd have to remember the ignore_index option.
def append_request ( requests : pd.DataFrame,
                     request  : pd.Series
                   ) -> pd.DataFrame:
    return ( requests
             . append ( request,
                        ignore_index = True ) )

# This turns out not to be necessary --
# there's no reason not to keep the entire history,
# which will be small.
def delete_oldest_request ( requests : pd.DataFrame
                          ) -> pd.DataFrame:
    # PITFALL: This doesn't verify that the oldest has been executed.
    # Upstream it should only be called if memory does not permit another run.
    # (If memory does not permit another run,
    # then at least the oldest request has been executed.)
    return ( canonicalize_requests( requests ) ) [1:]

def at_least_one_is_old ( requests : pd.DataFrame,
                          constraints : Dict[ str, str ]
                        ) -> bool:
    # PITFALL: Does not verify the old request was executed.
    # But it's only called if there's no space,
    # in which case we can assume the execution happened,
    # since execution is FIFO.
    now = datetime . now ()
    requests = canonicalize_requests( requests )
    oldest = requests . iloc[0] ["requested"]
      # Canonicalization ensures this is the oldest request.
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
                 . isnull ()
                 . all () )

def format_times ( requests : pd.DataFrame
                 ) -> pd.DataFrame:
    for c in ["requested","completed"]:
      requests [c] = pd.to_datetime( requests [c] )
    return requests
