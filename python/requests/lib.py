# TODO ? PITFALL: Much of this does IO, often destructively.
# Maybe I should make them functional and bump the IO
# into the calling code.

if True:
  from   datetime import datetime, timedelta
  import json
  import numpy as np
  import os
  import pandas as pd
  import subprocess
  from   typing import Callable, Dict, List, Set
  #
  import python.common.common as c
  import python.common.my_subproc as my_subproc


log_path = os.path.join ( c.tax_co_root,
                          "requests-log.txt" )

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

def read_requests ( requests_file_path : str
                  ) -> pd.DataFrame:
  if os . path . exists ( requests_file_path ):
    return format_times (
      pd . read_csv ( requests_file_path ) )
  else: return empty_requests ()

def write_requests ( reqs : pd.DataFrame,
                     requests_file_path : str ):
    ( canonicalize_requests ( reqs )
     . to_csv (
         requests_file_path,
         index = False ) )

def myZip (
    # PITFALL: All these file paths are relative to the user's folder.
    user_hash         : str,
    output_file       : str,
    input_files       : List[str],
    zip_instance_name : str, # Where this call to `zip` puts its logs in <user>/logs/<myZip_instance_name>/. This is an argument rather than hard-coded because myZip is called more than once per request -- once to zip logs and the config, and another time to zip the results.
):
  user_root = os.path.join (
    c.tax_co_root, "users", user_hash )

  zip_log_path = os.path.join ( user_root, "logs", zip_instance_name )

  os.makedirs ( zip_log_path, exist_ok = True )

  sp = my_subproc.run (
    to_run = ( # A list of strings effectively passed to bash
      [ "/usr/bin/zip", "-r", # The command and its options
        os.path.join ( user_root, output_file ) ] # The output path
      + [ os.path.join ( user_root, p ) # The input paths
          for p in input_files ]
    ),

    # PITFALL: Since these logs must be written after the zip command is run,
    # when I zip logs, the result will not include the log of the zip.
    log_path    = os.path.join ( zip_log_path, "log.txt"    ),
    stdout_path = os.path.join ( zip_log_path, "stdout.txt" ),
    stderr_path = os.path.join ( zip_log_path, "stderr.txt" ) )

def gb_used ( users_folder : str ) -> int:
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

def delete_oldest_folder_and_request (
    requests_path : str,
    users_folder : str ):
  # PITFALL: Order of the below matters. The oldest user folder can only
  # be found if the oldest request is still in the db.
  delete_oldest_user_folder (
    read_requests ( requests_path ),
    users_folder )
  mutate (
    requests_path,
    lambda reqs: delete_oldest_request (
      reqs ) )

def validate_users_folder ( users_folder : str):
    """Verify that users_folder looks plausible,
    to be sure it can't delete anything too important."""
    if users_folder[-1] == "/":
        users_folder = users_folder[:-1]
    (base, last) = os . path . split ( users_folder )
    if not last in ["users","users/"]:
      raise Exception ( users_folder + " does not end in `/users`" )
    if base . count ("/") != 2:
      raise Exception ( users_folder + " is not four folders below /." )

def delete_oldest_user_folder ( requests : pd.DataFrame,
                                users_folder : str ):
    validate_users_folder ( users_folder )
    requests = canonicalize_requests ( requests )
    oldest_user = requests . iloc[0] ["user"]
    with open( log_path, "a" ) as f:
        f.write( "Deleting oldest user, which is " + oldest_user + "\n" )
    subprocess.run (
        [ "rm",
          "-rf",
          os.path.join ( users_folder, oldest_user ) ] )

def this_request () -> pd.Series:
  """
  PITFALL: Looks pure, but in fact through the python.common lib
  it executes IO, reading the user's config file.
  """
  return pd . Series (
    { "user email"     : c.user_email,
        # Not necessary, but helpful to a human reading the data.
      "user"           : c.user,
      "subsample"      : c.subsample,
      "completed"      : False,
      "time requested" : datetime.now (),
      "time completed" : np.nan
    } )


#### #### #### #### #### #### #### #### #### ####
####  Pure-minus-reading-the-time functions  ####
#### #### #### #### #### #### #### #### #### ####

def mark_complete (
    user_hash : str,
    requests : pd.DataFrame ) -> pd.DataFrame:
  requests = requests . copy ()
  requests.loc [ requests [ "user" ] == user_hash,
                 "time completed" ] = (
     datetime . now () )
  requests.loc [ requests [ "user" ] == user_hash,
                 "completed" ] = True
  return requests

def at_least_one_result_is_old ( requests : pd.DataFrame,
                          constraints : Dict[ str, str ]
                        ) -> bool:
    # PITFALL: Does not verify the old request was executed.
    # But it's only called if there's no space,
    # in which case we can assume the execution happened,
    # since execution is FIFO.
    if (~requests["completed"]) . all():
        # If nothing is complete, no results exist, hence no results are old.
        return False
    else:
        now = datetime . now ()
        requests = canonicalize_requests ( requests )
        oldest_request_time = requests . iloc[0] ["time completed"]
          # Canonicalization ensures this comes from the oldest request.
        min_survival_time = (
            timedelta ( hours = 1 )
            * ( constraints[ "min_survival_minutes" ] / 60 ) )
        return (now - oldest_request_time) > min_survival_time


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
        columns = ["user email", "user","subsample","completed","time requested","time completed"] )

# Arguably this is too simple to be worth defining,
# but if I didn't, I'd have to remember the ignore_index option.
def append_request ( requests : pd.DataFrame,
                     request  : pd.Series
                   ) -> pd.DataFrame:
    requests = requests . copy ()
    return pd.concat ( [ requests,
                         pd.DataFrame ( request ) . transpose() ],
                       axis = "rows",
                       ignore_index = True )

# This might seem unnecessary -- why not just keep the old requests,
# since they're small? But they actually contain no information,
# because user names are hashes, and user configurations are deleted
# along with the data they requested.
#
# If we ever decide to keep old configurations,
# two more things would have to change:
# the request format would have to include a "(tabular data) deleted" field,
# and "delete oldest user()" would have to delete only the tabular data
# from the oldest request that still has such data.
# Or there might be an easier way, such as to simply copy the configs to another folder.
def delete_oldest_request ( requests : pd.DataFrame
                          ) -> pd.DataFrame:
    # PITFALL: This doesn't verify that the oldest has been executed.
    # Upstream it should only be called if memory does not permit another run.
    # (If memory does not permit another run,
    # then at least the oldest request has been executed.)
    return ( canonicalize_requests( requests ) ) [1:]

def canonicalize_requests ( requests : pd.DataFrame
                          ) -> pd.DataFrame:
    """ Calling this everywhere would be wasteful in big data,
    but it's negligible for the request data,
    and safer than assuming upstream functions have already done it."""
    requests = requests . copy ()
    return format_times (
        uniquify_requests ( requests )
        . sort_values (
            ["completed","time completed","time requested"],
            ascending = [False,    # Complete before incomplete.
                         True,     # Early before late.
                         True] ) ) # Early before late.

def uniquify_requests ( requests : pd.DataFrame
                      ) -> pd.DataFrame:
    requests = requests . copy ()
    return ( requests
        . sort_values (
            # Sort order doesn't matter for "user" or "completed";
            # every unique (user,completed) pair will be kept.
            # but it's important that within each such pair,
            # the first time is the earliest.
            ["user","completed","time requested"],
            ascending = True )
        . groupby( ["user","completed"] )
        . agg( "first" )
            # "ascending" means the first entry for a user is the earliest,
            # so the user keeps place in line after changing the request.
            # (This database does not know the content of the request,
            # just the time and the user.)
        . reset_index()
        [[ "user email", # Without this the grouping columns would be first.
           "user",
           "subsample",
           "completed",
           "time requested",
           "time completed" ]] )

def unexecuted_requests_exist ( requests : pd.DataFrame
                              ) -> bool:
    return ( (~ requests [ "completed" ] )
            . any () )

def next_request ( reqs : pd.DataFrame ) -> str:
    reqs = canonicalize_requests ( reqs )
    return ( reqs [ ~reqs [ "completed" ] ]
             . iloc[0] )

def format_times ( requests : pd.DataFrame
                 ) -> pd.DataFrame:
    requests = requests . copy ()
    for c in ["time requested","time completed"]:
      requests [c] = pd . to_datetime( requests [c] )
    return requests
