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
  from   datetime import datetime, timedelta
  import json
  import numpy as np
  import os
  import os.path as path
  import pandas as pd
  import subprocess
  import sys
  from   typing import Callable, Dict
  #
  import python.common.common as c
  import python.requests.lib  as lib


tax_co_root_folder = "/mnt/tax_co"
users_folder     = os.path.join ( tax_co_root_folder,
                                  "users/" )
constraints_file = os.path.join ( tax_co_root_folder,
                                  "data/constraints-time-memory.json" )
requests_file    = os.path.join ( tax_co_root_folder,
                                  "data/requests.csv" )
with open ( constraints_file ) as f:
    constraints = json . load ( f )

if len ( sys.argv ) > 1:
    lib . initialize_requests ( requests_file )
    print ( sys . argv [ 0 ] )
    print ( sys . argv [ 1 ] )
    action = sys . argv [ 2 ]

#    # for testing only
#    reqs = lib . append_request (
#        lib . empty_requests (),
#        lib . this_request () )

    if action == "add":
        lib . mutate (
            requests_file,
            lambda reqs: lib . append_request (
                reqs, lib . this_request () ) )

# TODO: something like this
#    if action == "delete":
#        lib . delete_oldest_user_folder (
#            reqs,
#            os . path . join ( users_folder,
#                               c . user ) )
