# PITFALL: This has nothing to do with the make.py package
# that is an alternative to the utility called make.
#
# Purpose: A Makefile cannot ingeest parameters from a .json file.
# But the Makefile needs to know those parameters,
# in order to track dependencies correclty -- for instance,
# products made from the 1/10 sample do not depend on products from 1/100.
# This solves that problem.

# USAGE:
#   Define targets here.
#   Define parameters in config/config.json
#     (or in a similar file in users/u<user-hash>/config/).
#   Run this:
#     PYTHONPATH="." python3 bash/run-makefile.py <config_file>
#   Usually, probably, that'll be this:
#     PYTHONPATH="." python3 bash/run-makefile.py users/jeff/config/config.json
#   but for debugging in a user folder, maybe something like this:
#     PYTHONPATH="." python3 bash/run-makefile.py users/1/config/config.json
#   If the <config_file> argument is not provided,
#   it defaults (in common.py) to "config/config.json".

import python.common.common as c
import os
import subprocess


tax_co_root_path    = "/mnt/tax_co"

targets = [ "show_config",
            "tests",
            # "show_params"
            "overview"
          ]
  # Makefile targets.
  # For the full list of possible targets,
  # see the Makefile, particularly the definition of .PHONY.

# TODO: This is duplicated in python/requests/main.py.
# Factor out both into a shared library.
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

subprocess.run (
  ( [ "make" ] +
    targets +
    [ "config_file" + "=" + c.config_file       ,
      "subsample"   + "=" + str( c.subsample )  ,
      "strategy"    + "=" + c.strategy          ,
      "regime_year" + "=" + str( c.regime_year ),
      "user"        + "=" + c.user ] ),
  env    = my_env,
  stdout = subprocess . PIPE,
  stderr = subprocess . PIPE )
