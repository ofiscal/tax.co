# SHARED MEMORY STRATEGY
# ######################
# The webpage (tax.co.web) adds requests to `requests.temp.csv`.
# Anything accessing that file uses a file lock for it.
# Such access is always brief; no process will make another wait long.
# #
# The microsimulation (tax.co) transfers files from `requests.temp.csv`
# to `requests.csv`. Then it processes those requests.
# It is the only process that manipulates `requests.csv`,
# so it doesn't need to worry about getting clobbered.

# PITFALL
# ######
# This Python program is meant to be called, either from another one --
# the Django server defined by the repo at
#   github.com:ofiscal/tax.co.web
# -- or by a cron job.

# How to invoke this code:
# ########################
# the first non-mandatory argument to `python3` at the command line
# should be a path to a user configuration,
# and the second should be an action to take.
# For example,
#   PYTHONPATH=/mnt/tax_co python3 python/requests/main.py users/1/config/shell.json add-to-temp-queue
#   PYTHONPATH=/mnt/tax_co python3 python/requests/main.py users/1/config/shell.json try-to-advance
# and for debugging:
#   PYTHONPATH=/mnt/tax_co python3 -m pdb python/requests/main.py users/1/config/shell.json try-to-advance

if True:
  from   datetime import datetime
  import filelock
  import json
  import os
  import pandas as pd
  import subprocess
  import sys
  #
  import python.requests.lib  as lib
  import python.common.common as c


tax_co_root_path    = "/mnt/tax_co"
process_marker_path = os.path.join ( tax_co_root_path,
                                     "data/request-ongoing" )
users_path          = os.path.join ( tax_co_root_path,
                                     "users/" )
constraints_path    = os.path.join ( tax_co_root_path,
                                     "data/constraints-time-memory.json" )
requests_path       = os.path.join ( tax_co_root_path,
                                     "data/requests.csv" )
requests_temp_path  = os.path.join ( tax_co_root_path,
                                     "data/requests.temp.csv" )
log_path            = os.path.join ( tax_co_root_path,
                                     "requests-log.txt" )
with open ( constraints_path ) as f:
    constraints = json . load ( f )

lock = filelock . FileLock ( requests_temp_path + ".lock" )
    # Since the file at requests_path is only ever manipulated by tax.co,
    # it does not need a lock. The one at requests_temp_path,
    # by contrast, is manipulated by tax.co.web also.
    # (Both only ever manipulate it through this program,
    # but more than one instance could be running at once.)

def transfer_requests_from_temp_queue ():
    with lock:
        reqs = lib . read_requests ( requests_path )
        reqs_temp = lib . read_requests ( requests_temp_path )
        reqs = lib . canonicalize_requests (
            pd . concat ( [reqs, reqs_temp] ) )
        lib . write_requests ( reqs,                    requests_path )
        lib . write_requests ( lib . empty_requests (), requests_temp_path )

def advance_request_queue ( user_hash : str ):
    with open ( process_marker_path, "w" ) as f:
        # Reserving this marker prevents another advance-the-queue
        # process from running while this one does.
        f . write ( user_hash )
    with open( log_path, "a" ) as f:
        f . write( "starting advance_request_queue\n" )
    user_root = os . path . join (
        tax_co_root_path, "users", user_hash )
    if True: # Refine the environment.
        my_env = os . environ . copy ()
        env_additions = ":" . join (
            [ tax_co_root_path,
              "/opt/conda/lib/python3.8/site-packages" ] )
              # TODO ? Why must this second folder be specified?
              # It's the default when I run python3 from the shell.
        my_env["PYTHONPATH"] = (
            ":" . join ( [ env_additions,
                           my_env [ "PYTHONPATH" ] ] )
            if "PYTHONPATH" in my_env . keys ()
            else env_additions )
    with open( log_path, "a" ) as f:
        f . write(
            "\n".join( [
                "About to run this:",
                "/opt/conda/bin/python3.8",
                "/mnt/tax_co/bash/run-makefile.py",
                os . path . join ( user_root, "config/shell.json" ),
                str( my_env ) ] )
            + "\n" )
    sp = subprocess.run (
        [ "/opt/conda/bin/python3.8",
            # TODO : Do I really have to specify this?
            # In the shell it's the default python (and the default python3).
          "/mnt/tax_co/bash/run-makefile.py",
          os . path . join ( user_root, "config/shell.json" ) ],
        env    = my_env,
        stdout = subprocess . PIPE,
        stderr = subprocess . PIPE )
    for ( path, source ) in [ ("stdout.txt", sp.stdout),
                              ("stderr.txt", sp.stderr) ]:
      with open ( os.path.join ( user_root, path ),
                  "a" ) as f:
        f . write ( source . decode () )
    if sp . returncode == 0:
        lib . mutate (
            requests_path,
            lambda reqs: lib . mark_complete (
                user_hash, reqs ) )
    os . remove ( process_marker_path )

def try_to_advance_request_queue ( user_hash : str ):
    # TODO: Test.
    with open( log_path, "a" ) as f:
        f . write( "starting try_to_advance_request_queue\n" )
    if os.path.exists ( process_marker_path ):
        with open( log_path, "a" ) as f:
            f.write( "Exit: An earlier process is still running.\n" )
        return ()
    reqs = lib . read_requests ( requests_path )
    if not lib.unexecuted_requests_exist ( reqs ):
        with open( log_path, "a" ) as f:
            f.write( "Exit: No unexecuted requests\n" )
        return ()
    elif lib . memory_permits_another_run (
            lib.gb_used ( users_path ),
            constraints ):
        with open( log_path, "a" ) as f:
            f.write( "Calling advance_request_queue\n" )
        advance_request_queue ( user_hash )
    elif lib.at_least_one_is_old ( reqs, constraints ):
        with open( log_path, "a" ) as f:
            f . write( "Deleting oldest request folder and request.\n" )
        lib.delete_oldest_folder_and_request (
            requests_path,
            users_path )
        try_to_advance_request_queue ( user_hash )
          # Recurse. Hopefully, now memory permits --
          # but since a user can choose a small sample size,
          # it might still not.
    else:
        with open( log_path, "a" ) as f:
            f . write ( "Exit: No free memory, and nothing old enough to delete.\n" )

if len ( sys.argv ) > 1:
    time_started = str( datetime.now () )
    action = sys . argv [ 2 ]
      # Arg 0 is the path to this program path, 1 the .json config.
      # Arg 1 is read and used by common.py.
    with open( log_path, "a" ) as f:
        f.write( "\n" )
        f.write( "Current GMT time: " + time_started  + "\n" )
        f.write( "Starting action " + action + "\n" )

    if True: # Initialize request data. (Usually unnecessary.)
      with open( log_path, "a" ) as f:
          f . write( "initializing data\n" )
      lib . initialize_requests ( requests_path )
      with lock:
          lib.initialize_requests ( requests_temp_path )
      with open( log_path, "a" ) as f:
          f . write( "initializing data: done\n" )

    # What the cron job does.
    if action == "try-to-advance":
        transfer_requests_from_temp_queue ()
        try_to_advance_request_queue ( c.user )

    # What the web page (the tax.co.web repo) does.
    if action == "add-to-temp-queue":
        with lock:
          lib.mutate (
              requests_temp_path,
              lambda reqs: lib . append_request (
                  reqs, lib . this_request () ) )

    with open( log_path, "a" ) as f:
        f.write( "Current time GMT: " + str( datetime.now() ) + "\n" )
        f.write( "Ending action " + action + "that began at time\n" )
        f.write( "    " + time_started  + "\n" )
