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
# This Python program is meant to be invoked either by
# (1) a cron job, or
# (2) another Python program -- specifically the Django server
#   defined by the repo at github.com:ofiscal/tax.co.web

# How to invoke this code:
# ########################
# the first non-mandatory argument to `python3` at the command line
# should be a path to a user configuration,
# and the second should be an action to take.
# For example,
#   PYTHONPATH=/mnt/tax_co:$PYTHONPATH python3 /mnt/tax_co/python/requests/main.py users/1/config/config.json add-to-temp-queue
#   PYTHONPATH=/mnt/tax_co:$PYTHONPATH python3 /mnt/tax_co/python/requests/main.py config/config.json try-to-advance-queue
#       config.json isn't used for try-to-advance-queue,
#       but still must be supplied, or common.py will be confused.
# and for debugging:
#   PYTHONPATH=/mnt/tax_co:$PYTHONPATH python3 -m pdb /mnt/tax_co/python/requests/main.py users/1/config/config.json try-to-advance-queue
#
# What the actions mean
# ---------------------
# add-to-temp-queue:
#   Appends the latest request to
#     data/requests.temp.csv
# try-to-advance-queue:
#   Runs the most recent incomplete request, if possible.
#   If there's no room for it and nothing old enough to be deleted,
#   or if another request is being processed, this does nothing.

if True:
  from   datetime import datetime
  import filelock
  import json
  import os
  import pandas as pd
  import subprocess
  import sys
  #
  import python.email
  import python.requests.lib  as lib
  import python.common.common as c
  import python.common.subprocess as my_subprocess


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
global_log_path     = os.path.join ( tax_co_root_path,
                                     "requests-log.txt" )
with open ( constraints_path ) as f:
    constraints = json . load ( f )

lock_for_temp_db = filelock . FileLock ( requests_temp_path + ".lock" )
    # Since the file at requests_path is only ever manipulated by tax.co,
    # it does not need a lock. The one at requests_temp_path,
    # by contrast, is manipulated by tax.co.web also.
    # (Both only ever manipulate it through this program,
    # but more than one instance could be running at once.)

def transfer_requests_from_temp_queue ():
    with lock_for_temp_db:
        reqs = lib . read_requests ( requests_path )
        reqs_temp = lib . read_requests ( requests_temp_path )
        reqs = lib . canonicalize_requests (
            pd . concat ( [reqs, reqs_temp] ) )
        lib . write_requests ( reqs,                    requests_path )
        lib . write_requests ( lib . empty_requests (), requests_temp_path )

def advance_request_queue ():
  user_hash : str = lib.next_request (
    lib.read_requests ( requests_path ) )
  with open ( process_marker_path, "w" ) as f:
    # Reserving this marker prevents another advance-the-queue
    # process from running while this one does.
    f . write ( user_hash )
  with open( global_log_path, "a" ) as f:
    f . write( "starting advance_request_queue\n" )
  user_root = os.path.join (
    tax_co_root_path, "users", user_hash )
  user_logs = os.path.join (
    user_root, "logs" )
  arq = "advance-request-queue" # Yes, just a string.

  sp = my_subprocess.run (
    to_run = [ "/opt/conda/bin/python3.8",
               # TODO : Do I really have to specify this?
               # In the shell it's the default python (and python3).
               "/mnt/tax_co/bash/run-makefile.py",
               os . path . join (
                 user_root, "config/config.json" ) ],
    log_path    = os.path.join ( user_logs, arq +        ".txt" ),
    stdout_path = os.path.join ( user_logs, arq + ".stdout.txt" ),
    stderr_path = os.path.join ( user_logs, arq + ".stderr.txt" ) )

  if True:
    # TODO : It would be better to run these only conditional on success.
    # `make` returns 0 even when from my point of view it didn't work,
    # so checking if `sp . returncode` is 0 is unreliable.
    #
    # TODO : Why is `sp` not defined after the above?
    # As of commit d2f0fd95286c970ee95f56c4fa633165324b2dca
    # it was working, before I factored my_subprocess.run() out of this.

    lib.zip_request_logs ( user_hash )
    data_path = os.path.join ( users_path, c.user, "data",
                               "recip-" + str(c.subsample) )
    python.email.send (
      receiver_address = c.user_email,
      subject = "Resultados de microsimulación",
      body = "Los resultados son los documentos .xlsx adjuntos. Si todo fue bien, los logs.zip no le van a importar.",
      attachment_paths = [
        os.path.join ( data_path, "overview.detail.2019.xlsx" ),
        os.path.join ( data_path, "overview_tmi.detail.2019.xlsx"),
        os.path.join ( data_path, "../..", "logs.zip" ) ] )
    lib.mutate (
      requests_path,
      lambda reqs: lib . mark_complete (
        user_hash, reqs ) )
    os.remove ( process_marker_path )

def try_to_advance_request_queue ( ):
    # TODO: Test.
    with open( global_log_path, "a" ) as f:
        f . write( "starting try_to_advance_request_queue\n" )
    if os.path.exists ( process_marker_path ):
        with open( global_log_path, "a" ) as f:
            f.write( "Exit: An earlier process is still running.\n" )
        return ()
    reqs = lib . read_requests ( requests_path )
    if not lib.unexecuted_requests_exist ( reqs ):
        with open( global_log_path, "a" ) as f:
            f.write( "Exit: No unexecuted requests\n" )
        return ()
    elif lib . memory_permits_another_run (
            lib.gb_used ( users_path ),
            constraints ):
        with open( global_log_path, "a" ) as f:
            f.write( "Calling advance_request_queue\n" )
        advance_request_queue () # RESUME HERE
    elif lib.at_least_one_result_is_old ( reqs, constraints ):
        with open( global_log_path, "a" ) as f:
            f . write( "Deleting oldest request folder and request.\n" )
        lib.delete_oldest_folder_and_request (
            requests_path,
            users_path )
        try_to_advance_request_queue ()
          # Recurse. Hopefully, now memory permits --
          # but since a user can choose a small sample size,
          # it might still not.
    else:
        with open( global_log_path, "a" ) as f:
            f . write ( "Exit: No free memory, and nothing old enough to delete.\n" )

if len ( sys.argv ) > 1:
    time_started = str( datetime.now () )
    action = sys . argv [ 2 ]
      # Arg 0 is the path to this program path, 1 the .json config.
      # Arg 1 is read and used by common.py.
    with open( global_log_path, "a" ) as f:
        f.write( "\n" )
        f.write( "Current time: " + time_started  + "\n" )
        f.write( "Starting action " + action + "\n" )

    if True: # Initialize request data. (Usually unnecessary.)
      with open( global_log_path, "a" ) as f:
          f . write( "initializing data\n" )
      lib . initialize_requests ( requests_path )
      with lock_for_temp_db:
          lib.initialize_requests ( requests_temp_path )
      with open( global_log_path, "a" ) as f:
          f . write( "initializing data: done\n" )

    # What the cron job does.
    if action == "try-to-advance-queue":
        transfer_requests_from_temp_queue ()
        try_to_advance_request_queue ()

    # What the web page (the tax.co.web repo) does.
    if action == "add-to-temp-queue":
        with lock_for_temp_db:
          lib.mutate (
              requests_temp_path,
              lambda reqs: lib . append_request (
                  reqs, lib . this_request () ) )

    with open( global_log_path, "a" ) as f:
        f.write( "Current time: " + str( datetime.now() ) + "\n" )
        f.write( "Ending action " + action + "that began at time\n" )
        f.write( "    " + time_started  + "\n" )
