if True:
  import pandas as pd
  import numpy as np
  import weightedcalcs as weightLib
  #
  import python.build.classes as cl
  import python.common.common as cm
  import python.build.output_io as oio
  from python.common.util import noisyQuantile
  from python.common.describe import describeWithMissing
  import python.report.time_to_save_for_a_month.defs as defs


income = ( # choose one
    "income"
    # "income, cash"
    # "ICMDUG"
    )
spending = ( # choose one
    "value, purchase"
    # "GCMUG"
    )

wc = weightLib.Calculator('weight')

hh = oio.readStage(
    cm.subsample
  , "households_2_purchases." + cm.strategy_year_suffix )

hh = hh[ ~ ( hh["income"].isnull()
           | hh["value, purchase"].isnull() ) ]

hh["months to save for a month"] = hh.apply(
    lambda row: defs.months_to_save_for_a_month(
        income = row["income"],
        spending = row["value, purchase"] ),
    axis = "columns" )

hh["months to save for a month, cash"] = hh.apply(
    lambda row: defs.months_to_save_for_a_month(
        income = row["income, cash"],
        spending = row["value, purchase"] ),
    axis = "columns" )

if True: # explore
  hh["months to save for a month"].describe()
  hh["used savings"].describe()
  hh["recently bought this house"].describe()
  #
  len(hh)
  len( hh[ hh["used savings"] > 0 ] )
  len( hh[ hh["recently bought this house"] > 0 ] )

# Just under 7% of households used their savings.
len( hh[ hh["used savings"] > 0 ] ) / len(hh)
# Drop them.
hh = hh[ hh["used savings"] <= 0 ]
hh = hh.drop( columns = ["used savings"] )

deciles = list( np.round(
    np.arange( 0.1, 1, 0.1 ),
    1 ) )

zoom_quantiles = list( np.round(
    np.arange( 0.32, 0.45001, 0.01 ),
    2 ) )

if True:
  assert cm.subsample == 1
  every = defs.quantiles_report(
      defs.mk_samples(
          # full sample gives just about identical results
          hh[ hh["recently bought this house"] <= 0 ] ),
      "months to save for a month, cash",
      wc,
      deciles,
      add_unity = True )
  zoom = defs.quantiles_report(
      defs.mk_samples(
          # full sample gives just about identical results
          hh[ hh["recently bought this house"] <= 0 ] ),
      "months to save for a month, cash",
      wc,
      zoom_quantiles )

# Including non-cash income would seem to compare apples and oranges,
# although the results are largely the same.
#
# every_ = defs.quantiles_report(
#     defs.mk_samples(
#         # full sample gives just about identical results
#         hh[ hh["recently bought this house"] <= 0 ] ),
#     "months to save for a month",
#     wc,
#     deciles,
#     add_unity = True )
#
# zoom_ = defs.quantiles_report(
#     defs.mk_samples(
#         # full sample gives just about identical results
#         hh[ hh["recently bought this house"] <= 0 ] ),
#     "months to save for a month",
#     wc,
#     zoom_quantiles )


############## How much money the extreme savers make ##############

q = wc.quantile( hh, # the top decile of savers
        "months to save for a month, cash",
        0.1 )

high_savers = hh[ hh[ "months to save for a month, cash" ] < q ]
high_savers["income, cash"].describe()

for q in np.arange(0,1,0.05):
  print( round( q*100),
         round( wc.quantile( high_savers, "income, cash", q ) ) )

high_saving_poor = hh [
     (hh[ "months to save for a month, cash" ] < q) &
     (hh[ "income, cash" ] < 5e5) ]

# The poorest high-savers aren't surviving on in-kind income we know about.
# Nor are they receiving non-purchase goods sufficient to bring their
# incomes to something one might consider
( high_saving_poor
  [[ "income, in-kind", "value, non-purchase"]]
  . describe() )

