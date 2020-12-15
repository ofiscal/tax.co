# This has nothing to do with the make.py package
# that is an alternative to the utility called make.
#
# Purpose: A Makefile cannot ingeest parameters from a .json file.
# But the Makefile needs to know those parameters,
# in order to track dependencies correclty -- for instance,
# products made from the 1/10 sample do not depend on products from 1/100.
# This solves that problem.
#
# Usage:
#   Define targets here.
#   Define parameters in config.json or similar.
#   Run this:
#     PYTHONPATH="." python3 bash/run-makefile.py <config_file>
#   If the <config_file> argument is not provided,
#   it defaults (in common.py) to "repl_params.py".

import python.common.common as common
import os


targets = "tests overview"
  # A space-separated list of Makefile targets.
  # Likely values include "tests" and "overview".
  # For the full list of possible targets,
  # see the Makefile, particularly the definition of .PHONY.

os.system( "make "         + targets                 +
           " config_file=" + common.config_file      +
           " subsample="   + str( common.subsample ) +
           " strategy="    + common.strategy         +
           " regime_year=" + str( common.regime_year )
  )
