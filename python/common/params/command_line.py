import sys
import python.common.terms as t


strategy_names = [ # There used to be a lot of these.
  t.detail,        # They disappeared in the branch "retire-hypotheticals".
  t.vat_holiday_1,
  t.vat_holiday_2,
  t.vat_holiday_3
]

subsample = int( sys.argv[1] )
if not subsample in [1,10,100,1000]:
  raise ValueError( "invalid subsample reciprocal: " + str(subsample) )

strategy = sys.argv[2]
if not strategy in strategy_names:
  raise ValueError( "invalid strategy: " + strategy )

regime_year = int( sys.argv[3] )
if not regime_year in [2016, 2018]:
  raise ValueError( "invalid tax regime year: " + str(regime_year) )

strategy_suffix = strategy
strategy_year_suffix = strategy + "." + str(regime_year)

