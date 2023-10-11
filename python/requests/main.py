"""
SHARED MEMORY STRATEGY
######################
The webpage (tax.co.web) adds requests to `requests.temp.csv`.
Anything accessing that file uses a file lock for it.
Such access is always brief; no process will make another wait long.
#
The microsimulation (tax.co) transfers files from `requests.temp.csv`
to `requests.csv`. Then it processes those requests.
It is the only process that manipulates `requests.csv`,
so it doesn't need to worry about getting clobbered.

PITFALL: Invocation is weird
############################
This Python program is meant to be invoked either by
(1) a cron job, or
(2) another Python program -- specifically the Django server
  defined by the repo at github.com:ofiscal/tax.co.web

PITFALL: Limitations in definitions from python.common.common
#############################################################
That program defines some things like "strategy"
that depend on the user's config file.
But this program is invoked without knowing which is that config file.
References within this file to those user-dependent definitions,
therefore, are a bad idea.

How to invoke this code:
########################
The first non-mandatory argument to `python3` at the command line
should be a path to a user configuration,
and the second should be an action to take.
For example,
  PYTHONPATH=/mnt/tax_co:$PYTHONPATH python3 /mnt/tax_co/python/requests/main.py users/symlinks/jbb/config/config.json add-to-temp-queue
  PYTHONPATH=/mnt/tax_co:$PYTHONPATH python3 /mnt/tax_co/python/requests/main.py config/config.json try-to-advance-queue
      config.json isn't used for try-to-advance-queue,
      but still must be supplied, or common.py will be confused.
and for debugging:
  PYTHONPATH=/mnt/tax_co:$PYTHONPATH python3 -m pdb /mnt/tax_co/python/requests/main.py users/symlinks/jbb/config/config.json try-to-advance-queue

What the actions mean
---------------------
add-to-temp-queue:
  Appends the latest request to
    data/requests.temp.csv
try-to-advance-queue:
  Runs the most recent incomplete request, if possible.
  If there's no room for it and nothing old enough to be deleted,
  or if another request is being processed, this does nothing.

How to debug this code
######################
Set up a desirable user data state,
and save it via the scripts in state/.
Stop the cron job.
Set an appropriate breakpoint (pdb.set_trace).
"""

if True:
  from   datetime import datetime
  import filelock
  import glob
  import json
  import os
  import pandas as pd
  import sys
  from   typing import List, Set, Dict
  #
  import python.common.common      as c
  import python.common.my_subproc  as my_subproc
  import python.email
  import python.requests.lib       as lib
  import python.requests.defs      as defs


with open ( defs.constraints_path ) as f:
    constraints = json . load ( f )

lock_for_temp_db = filelock . FileLock ( defs.requests_temp_path + ".lock" )
    # Since the file at defs.requests_path is only ever manipulated by tax.co,
    # it does not need a lock. The one at defs.requests_temp_path,
    # by contrast, is manipulated by tax.co.web also.
    # (Both only ever manipulate it through this program,
    # but more than one instance could be running at once.)
    #
    # PITFALL: This lock file will persist even when no process holds it.
    # That's not a problem.

def transfer_requests_from_temp_queue ():
  """
  Moves all requests from the temp queue (.csv file)
  to the permanent queue.
  """
  with lock_for_temp_db:
    reqs = lib . read_requests ( defs.requests_path )
    reqs_temp = lib . read_requests ( defs.requests_temp_path )
    reqs = lib . canonicalize_requests (
      pd . concat ( [reqs, reqs_temp] ) )
    lib . write_requests ( reqs,                    defs.requests_path )
    lib . write_requests ( lib . empty_requests (), defs.requests_temp_path )

# TODO: Factor out some functions (e.g. emailing).
def advance_request_queue ():
  """
  Read the next request.
  Create a powerless lock at "data/request-ongoing".
  Call `python/run-makefile.py` per the request.
  Zip some files.
  Email results to user.
  Mark the request complete in `requests.csv`.
  Remove the powerless lock at "data/request-ongoing".
  Do logging throughout.
  """

  req =  lib.next_request (
    lib.read_requests ( defs.requests_path ) )
  with open ( defs.process_marker_path, "w" ) as f:
    # Reserving this marker prevents another advance-the-queue
    # process from running while this one does.
    f . write ( req["user"] )
  with open( defs.global_log_path, "a" ) as f:
    f . write( "Starting advance_request_queue.\n" )
  user_root = os.path.join (
    c.tax_co_root, "users", req["user"] )
  user_logs = os.path.join (
    user_root, "logs" )
  arq = "advance-request-queue" # Some filenames use this.

  sp = my_subproc.run (
    to_run = [
      "python3",
      os.path.join ( c.tax_co_root,
                     "python/run-makefile.py" ),
      os . path . join (
        user_root, "config/config.json" ) ],
    log_path    = os.path.join ( user_logs,
                                 arq +        ".txt" ),
    stdout_path = os.path.join ( user_logs,
                                 arq + ".stdout.txt" ),
    stderr_path = os.path.join ( user_logs,
                                 arq + ".stderr.txt" ) )
  with open( defs.global_log_path, "a" ) as f:
    f . write( "Subprocess: Done.\n" )

  if True:
    # TODO : Better to run these only conditional on success.
    # `make` returns 0 even if (to me) it didn't work,
    # so checking if `sp . returncode` is 0 is unreliable.
    #
    # TODO : Why is `sp` not defined after the above?
    # As of commit d2f0fd95286c970ee95f56c4fa633165324b2dca
    # it was working, before I factored my_subproc.run() out of this.
    data_path = os.path.join (
      defs.users_path, req["user"], "data",
      "recip-" + str( req["subsample"] ) )
    lib.myZip (
      user_hash = req["user"],
      output_file = "results.zip",
      input_files = (
        glob.glob   ( os.path.join ( data_path, "report*.csv"  ) )
        + glob.glob ( os.path.join ( data_path, "change*.png"  ) )
        + glob.glob ( os.path.join ( data_path, "changes*.csv" ) ) ),
      zip_instance_name = "zipping-results", )
    with open( defs.global_log_path, "a" ) as f:
      f . write( "Zipping the results: done.\n" )

    lib.myZip (
      user_hash = req["user"],
      output_file = os.path.join ( user_root, "config-and-logs.zip" ),
      input_files = [ os.path.join ( user_root, "logs" ),
                      os.path.join ( user_root, "config" ), ],
      zip_instance_name = "zipping-config-and-logs", )
    with open( defs.global_log_path, "a" ) as f:
      f . write( "Zipping the config and logs: done.\n" )

    with open( defs.global_log_path, "a" ) as f:
      f . write( "About to send attachemnts at "
                 + data_path + ".\n" )
    if not ( req["user email"] == "quien@donde.net" ):
      # If the email address is quien@donde.net, then the user didn't change
      # the default email address. Sending would fail.
      # This might be getting triggered by bots, and if the website
      # ever became popular, could become a problem,
      # since Gmail only lets me send so many automatic emails per day.
      python.email.send (
        receiver_address = req["user email"],
        subject = "Resultados de microsimulación",
        body = defs.email_body,
        attachment_paths = [
          os.path.join ( data_path, "../../config-and-logs.zip" ),
          os.path.join ( data_path, "../../results.zip" ) ], )
      with open( defs.global_log_path, "a" ) as f:
        f . write( "Email: Done.\n" )

    lib.mutate (
      defs.requests_path,
      lambda reqs: lib . mark_complete (
        req["user"], reqs ) )
    with open( defs.global_log_path, "a" ) as f:
      f . write( "Mutate requests db: Done.\n" )

    os.remove ( defs.process_marker_path )
    with open( defs.global_log_path, "a" ) as f:
      f . write( "Remove process marker: Done.\n" )

# TODO: Test.
def try_to_advance_request_queue ():
  """
  If the powerless lock `data/request-ongoing` exists, stop.
  If there are no unexecuted requests, stop.
  If memory permits another run,
    run advance_request_queue() and stop.
  If memory does not permit another run,
    but some request is old enough to delete,
    then delete that request and its folder,
    and recurse: `try_to_advance_request_queue()`.
  Otherwise stop.
  """
  with open( defs.global_log_path, "a" ) as f:
    f . write( "starting try_to_advance_request_queue\n" )
  if os.path.exists ( defs.process_marker_path ):
    with open( defs.global_log_path, "a" ) as f:
      f.write( "Exit: An earlier process is still running.\n" )
    return ()
  reqs = lib . read_requests ( defs.requests_path )
  if not lib.unexecuted_requests_exist ( reqs ):
    with open( defs.global_log_path, "a" ) as f:
      f.write( "Exit: No unexecuted requests\n" )
    return ()
  if lib . memory_permits_another_run (
      lib.gb_used ( defs.users_path ),
      constraints ):
    with open( defs.global_log_path, "a" ) as f:
      f.write( "Calling advance_request_queue\n" )
    advance_request_queue ()
  elif lib.at_least_one_result_is_old ( reqs, constraints ):
    with open( defs.global_log_path, "a" ) as f:
      f . write(
        "Deleting oldest request folder and request.\n" )
    lib.delete_oldest_folder_and_request (
      defs.requests_path, defs.users_path )
    try_to_advance_request_queue ()
      # Recurse. Hopefully, now memory permits --
      # but since a user can choose a small sample size,
      # it might still not.
  else:
    with open( defs.global_log_path, "a" ) as f:
      f . write (
        "Exit: No free memory, and nothing old enough to delete.\n" )

def request_handler ():
  """
  Initialize request queues.
    Since they usually already exist,
    this is usually unnecessary, but it's cheap.
  if action == "try-to-advance-queue":
    transfer_requests_from_temp_queue ()
    try_to_advance_request_queue ()
    This action is called every minute from a cron job.
  if action == "add-to-temp-queue":
    Do that.
    This action is called whenever a user submits a request online.
  Do logging throughout.
  """

  time_started = str( datetime.now () )
  action = sys . argv [ 2 ]
    # Arg 0 is the path to this program path, 1 the .json config.
    # Arg 1 is read and used by common.py.
  with open( defs.global_log_path, "a" ) as f:
    f.write( "\n" )
    f.write( "Current time: " + time_started  + "\n" )
    f.write( "Starting action " + action + "\n" )

  if True: # Initialize request data. (Usually unnecessary, but cheap.)
    with open( defs.global_log_path, "a" ) as f:
      f . write( "Initializing data.\n" )
    lib . initialize_requests ( defs.requests_path )
    with lock_for_temp_db:
      lib.initialize_requests ( defs.requests_temp_path )
    with open( defs.global_log_path, "a" ) as f:
      f . write( "Initializing data: Done.\n" )

  # What the cron job does.
  if action == "try-to-advance-queue":
    transfer_requests_from_temp_queue ()
    try_to_advance_request_queue ()

  # What the web page (the tax.co.web repo) does.
  if action == "add-to-temp-queue":
    with lock_for_temp_db:
      lib.mutate (
        defs.requests_temp_path,
        lambda reqs: lib . append_request (
          reqs, lib . this_request () ) )

  with open( defs.global_log_path, "a" ) as f:
    f.write( "Current time: " + str( datetime.now() ) + "\n" )
    f.write( "Ending action \"" + action + "\" that began at time\n" )
    f.write( "    " + time_started  + "\n" )

if len ( sys.argv ) > 1:
  request_handler ()
