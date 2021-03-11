# SHARED MEMORY STRATEGY
# ######################
# The webpage (tax.co.web) adds requests to `requests.temp.csv`.
# Anything accessing that file uses a file lock for it.
# Such access is always brief; no process will make another wait long.
#
# The microsimulation (tax.co) transfers files from `requests.temp.csv`
# to `requests.csv`. Then it processes those requests.
# It is the only process that manipulates `requests.csv`,
# so it doesn't need to worry about getting clobbered.

# PITFALL
# ######
# This Python program is meant to be called from another one --
# particularly, by a program in the repo at
#   github.com:ofiscal/tax.co.web
# -- rather than by hand.
#
# How to use this
# ###############
# the first non-mandatory argument to `python3` at the command line
# should be a path to a user configuration,
# and the second should be an action to take.
# For example,
#
#   PYTHONPATH="." python3 python/requests/main.py users/jeff/config/shell.json add

if True:
  import filelock
  import json
  import os
  import pandas as pd
  import sys
  from   typing import Callable, Dict
  #
  import python.requests.lib  as lib


tax_co_root_folder = "/mnt/tax_co"
users_folder     = os.path.join ( tax_co_root_folder,
                                  "users/" )
constraints_file = os.path.join ( tax_co_root_folder,
                                  "data/constraints-time-memory.json" )
requests_file    = os.path.join ( tax_co_root_folder,
                                  "data/requests.csv" )
requests_temp_file = os.path.join ( tax_co_root_folder,
                                    "data/requests.temp.csv" )
with open ( constraints_file ) as f:
    constraints = json . load ( f )

def transfer_requests_from_temp_queue ():
    lock = filelock . FileLock ( requests_temp_file + ".lock" )
      # Since requests_file is only ever manipulated by tax.co,
      # it does not need a lock. requests_temp_file, OTOH,
      # is manipulated by tax.co.web also.
    with lock:
        for f in [ requests_file, requests_temp_file ]:
            lib . initialize_requests ( f )
        reqs = lib . read_requests ( requests_file )
        reqs_temp = lib . read_requests ( requests_temp_file )
        reqs = lib . canonicalize_requests (
            pd.concat ( [reqs, reqs_temp] ) )
        lib . write_requests ( reqs,                    requests_file )
        lib . write_requests ( lib . empty_requests (), requests_temp_file )

def advance_request_queue ():
    pass # TODO: Run makefile, mark the request executed.

def try_to_advance_request_queue ():
    # TODO: Test.
    reqs = lib . read_requests ( requests_file )
    if not unexecuted_requests_exist ( reqs ):
        return ()
    if lib .  memory_permits_another_run (
            lib . gb_used ( users_folder ),
            constraints ):
        advance_request_queue ()
    elif lib . at_least_one_is_old ( reqs, constraints ):
        delete_oldest_user_folder ( requests_file, users_folder )
        try_to_advance_request_queue ()
          # Recurse. Hopefully, now memory permits --
          # but since a user can choose a small sample size,
          # it might still not.

if len ( sys.argv ) > 1:
    lib . initialize_requests ( requests_file )
    print ( sys . argv [ 0 ] )
    print ( sys . argv [ 1 ] )
    action = sys . argv [ 2 ]

    if action == "add-to-queue":
        lib . mutate (
            requests_file,
            lambda reqs: lib . append_request (
                reqs, lib . this_request () ) )
