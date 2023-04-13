"""
This program has nothing to do with the make.py package
that is an alternative to the utility called make.

PURPOSE: A Makefile cannot ingest .json parameters.
But the Makefile needs to know those parameters,
in order to track dependencies correctly -- for instance,
products made from the 1/10 sample do not depend on products from 1/100.
This solves that problem.

USAGE:
  Optional: Change the targets defined in this file.
    See the `targets` variable below.
  Optional: Define parameters in config/config.json,
    or in a similar file in users/u<user-hash>/config/
  From the root folder of the project, run this:
    PYTHONPATH="." python3 bash/run-makefile.py <config_file>
    for instance:
      PYTHONPATH="." python3 bash/run-makefile.py users/symlinks/jbb/config/config.json
  The file path in <>s is optional.
    If you don't provide it, it will default to config/config.json.

PITFALL:
  If, when you run the above, you receive an error of the form
  "No such file or directory:
    '/mnt/tax_co/users/ue01af9d7df5e7e220c6ef60e400a6683/logs/make.txt"
  it's because the program expects `users/ue01af9d7df5e7e220c6ef60e400a6683/`
  to exist, and to have the same structure as `users/example/`
  The easiest way to solve this is to use the web UI,
  which creates that folder automatically.
  Another way is to copy `users/example/` folder to
  `users/ue01af9d7df5e7e220c6ef60e400a6683/` (or whatever appeared in the error),
  and then editing the `config.json` file within it.
"""

from   datetime import datetime
import os
import subprocess
from   typing import List

import python.common.common     as c
import python.common.terms      as terms
import python.makefile_targets  as makefile_targets


tax_co_root_path    = "/mnt/tax_co"

# TODO: Some of this is duplicated,
# in a less functional idiom, in python/requests/main.py.
# Factor out both into a shared library.
if True: # Refine the environment.
  my_env = os . environ . copy ()
  env_additions = ":" . join (
    [ tax_co_root_path ] )
  my_env["PYTHONPATH"] = (
      ":" . join ( [ env_additions,
                     my_env [ "PYTHONPATH" ] ] )
      if "PYTHONPATH" in my_env . keys ()
      else env_additions )

def run_one_config (
    config_file : str,
    subsample   : int,
    strategy    : str,
    regime_year : int,
    user_hash   : str,
    targets     : List[str] ):

  # logging
  logs_path = os.path.join(
    tax_co_root_path, "users", user_hash, "logs" )
  with open( os.path.join( logs_path, "make.txt"),
             "a" ) as f:
    f.write( "make.py starting at " + str( datetime.now() ) + "\n" )

  # Run the Makefile.
  # PITFALL: It uses the config file provided to subprocess.run,
  # not necessarily the one used when this file was invoked.
  sp = subprocess.run (
    ( [ "/usr/bin/make" ] +
      targets +
      [
        # "--dry-run",
        "config_file" + "=" + config_file,
        "subsample"   + "=" + str( subsample ),
        "strategy"    + "=" + strategy,
        "regime_year" + "=" + str( regime_year ),
        "user"        + "=" + user_hash,
        # "-k" # Keep going with other targets after any fails, if possible.
       ] ),
    cwd    = tax_co_root_path,
    env    = my_env,
    stdout = subprocess . PIPE,
    stderr = subprocess . PIPE )

  # logging
  for ( name, source ) in [ ("make.stdout.txt", sp.stdout),
                            ("make.stderr.txt", sp.stderr) ]:
    with open ( os.path.join ( logs_path, name ),
               "a" ) as f:
      f . write ( source . decode () )
  with open( os.path.join( logs_path, "make.txt"),
             "a" ) as f:
    f.write( "make.py ending at " + str( datetime.now() ) + "\n" )

run_one_config ( # First rebuild the baseline, if appropriate.
                 # Use the full sample every time.
  config_file = "users/symlinks/baseline/config/config.json",
  subsample   = c.subsample,
    # PITFALL: This parameter, which dictates the subsample size used
    # when generating the baseline model, is drawn not from that config file,
    # but instead from the user's. The two config files
    # must have the same sample size.
    # (Otherwise the wrong baseline targets will be made.)
  strategy    = terms.detail,
  regime_year = 2019,
  user_hash   = c.user_hash_from_email ( "baseline" ),
  targets     = makefile_targets.targets )

run_one_config ( # Then build the user data.
  config_file = c.config_file,
  subsample   = c.subsample,
  strategy    = c.strategy,
  regime_year = c.regime_year,
  user_hash   = c.user,
  targets     = (
    makefile_targets.targets
    + ( [] # Since the baseline user is the one others are compared to,
        # it makes no sense to build "compare" for tthat user.
        if c.user_email == "baseline"
        else ["compare"] ) ) )
