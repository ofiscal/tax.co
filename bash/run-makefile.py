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
import subprocess


targets = [ "show_config",
            "tests",
            # "show_params"
            "overview"
          ]
  # Makefile targets.
  # For the full list of possible targets,
  # see the Makefile, particularly the definition of .PHONY.

subprocess.run (
    [ "make",
     "bash/run-makefile.py" ] +
    targets +
    [ "config_file=" + c.config_file       ,
      "subsample="   + str( c.subsample )  ,
      "strategy="    + c.strategy          ,
      "regime_year=" + str( c.regime_year ),
      "user="        + c.user ]
    )
