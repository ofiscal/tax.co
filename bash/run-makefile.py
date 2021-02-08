# PITFALL: This has nothing to do with the make.py package
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
#   Define parameters in config/shell.json or similar.
#   Run this:
#     PYTHONPATH="." python3 bash/run-makefile.py <config_file>
#   Usually, probably, that'll be this:
#     PYTHONPATH="." python3 bash/run-makefile.py users/jeff/shell.json
#   If the <config_file> argument is not provided,
#   it defaults (in common.py) to "config/repl.json".

import python.common.common as c
import os


targets = "show_config tests overview" # show_params
  # A space-separated list of Makefile targets.
  # Likely values include "tests" and "overview".
  # For the full list of possible targets,
  # see the Makefile, particularly the definition of .PHONY.

os.system(
    "make " # + " --keep-going " +
    + targets                 +
    " config_file="           + c.config_file           +
    " subsample="             + str( c.subsample )      +
    " strategy="              + c.strategy              +
    " regime_year="           + str( c.regime_year )    +
    " vat_by_coicop="         + c.vat_by_coicop         +
    " vat_by_capitulo_c="     + c.vat_by_capitulo_c     +
    " marginal_rates_folder=" + c.marginal_rates_folder +
    " user="                  + c.user
    )
