# PITFALL: This has nothing to do with the make.py package
# that is an alternative to the utility called make.
#
# PURPOSE: A Makefile cannot ingeest .json parameters.
# But the Makefile needs to know those parameters,
# in order to track dependencies correclty -- for instance,
# products made from the 1/10 sample do not depend on products from 1/100.
# This solves that problem.

# USAGE:
#   Optional: Change the targets defined in this file.
#     See the `targets` variable below.
#   Optional: Define parameters in config/config.json,
#     or in a similar file in users/u<user-hash>/config/
#   From the root folder of the project, run this:
#     PYTHONPATH="." python3 bash/run-makefile.py <config_file>
#   The file path in <>s is optional; if you don't provide it,
#     it will default to config/config.json.
#
# PITFALL:
#   If, when you run the above, you receive an error of the form
#   "No such file or directory:
#     '/mnt/tax_co/users/ue01af9d7df5e7e220c6ef60e400a6683/logs/make.txt"
#   it's because the program expects `users/ue01af9d7df5e7e220c6ef60e400a6683/`
#   to exist, and to have the same structure as `users/example/`
#   Solve this by copying `users/example/` folder to
#   `users/ue01af9d7df5e7e220c6ef60e400a6683/` (or whatever appeared in the error),
#   and then editing the `config.json` file within it.

from   datetime import datetime
import os
import python.common.common as c
import subprocess


tax_co_root_path    = "/mnt/tax_co"

logs_path = os.path.join(
  tax_co_root_path, "users", c.user, "logs" )

with open( os.path.join( logs_path, "make.txt"),
           "a" ) as f:
  f.write( "make.py starting at " + str( datetime.now() ) + "\n" )

targets = [ "show_config",
            "show_params",
            "tests",
            "report_households"
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
        "/opt/conda/lib/python3.9/site-packages" ] )
        # TODO ? Why must this second folder be specified?
        # It's the default when I run python3 from the shell.
  my_env["PYTHONPATH"] = (
      ":" . join ( [ env_additions,
                     my_env [ "PYTHONPATH" ] ] )
      if "PYTHONPATH" in my_env . keys ()
      else env_additions )

sp = subprocess.run (
  ( [ "/usr/bin/make" ] +
    targets +
    [ "config_file" + "=" + c.config_file       ,
      "subsample"   + "=" + str( c.subsample )  ,
      "strategy"    + "=" + c.strategy          ,
      "regime_year" + "=" + str( c.regime_year ),
      "user"        + "=" + c.user,
      "-k" # Keep going with other targets after any fails, if possible.
     ] ),
  cwd    = tax_co_root_path,
  env    = my_env,
  stdout = subprocess . PIPE,
  stderr = subprocess . PIPE )

for ( name, source ) in [ ("make.stdout.txt", sp.stdout),
                          ("make.stderr.txt", sp.stderr) ]:
  with open ( os.path.join ( logs_path, name ),
             "a" ) as f:
    f . write ( source . decode () )

with open( os.path.join( logs_path, "make.txt"),
           "a" ) as f:
  f.write( "make.py ending at " + str( datetime.now() ) + "\n" )
