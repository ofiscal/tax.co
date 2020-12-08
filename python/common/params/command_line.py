# What to import if working from the command line.
# In this case there are command-line arguments to interpret,
# hence the calls to `sys.argv`.

import sys
import python.common.terms as terms


valid_strategies = [ # There used to be a lot of these.
  terms.detail       # They disappeared in the branch "retire-hypotheticals".
]

subsample = int( sys.argv[1] )
if not subsample in [1,10,100,1000]:
  raise ValueError( "invalid subsample reciprocal: " + str(subsample) )

strategy = sys.argv[2]
if not strategy in strategy_names:
  raise ValueError( "invalid strategy: " + strategy )

regime_year = int( sys.argv[3] )
if not regime_year in [2016, 2018, 2019]:
  raise ValueError( "invalid tax regime year: " + str(regime_year) )

strategy_suffix = strategy
strategy_year_suffix = strategy + "." + str(regime_year)
