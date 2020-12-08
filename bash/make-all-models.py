# This has nothing to do with the make.py package
# that is an alternative to the utility called make.
#
# Purpose: A Makefile cannot ingeest parameters from a .json file.
# But the Makefile needs to know those parameters,
# in order to track dependencies correclty -- for instance,
# products made from the 1/10 sample do not depend on products from 1/100.
# This solves that problem.
#
# TODO Usage: PYTHONPATH="." python3 bash/make.py

import python.common.common
import os
import sys


# See the definitions of common.common.valid* for what values work here.
subsample = 1
regime_year = 2019
strategy = "detail"
config_file = "config.json"

target = "tests" # Likely targets include "tests" and "overview".
                 # See Makefile for full list of possible targets,
                 # in particular the definition of .PHONY.

os.system( "make "         + target           +
           " config_file=" + config_file      +
           " subsample="   + str( subsample ) +
           " strategy="    + strategy         +
           " regime_year=" + str( regime_year )
  )
