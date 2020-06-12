if True:
  import pandas as pd
  import numpy as np
  from typing import List, Tuple
  #
  import python.build.classes as cl
  import python.common.common as cm
  import python.build.output_io as oio
  from python.common.util import noisyQuantile
  from python.common.describe import describeWithMissing
  import matplotlib
  import matplotlib.pyplot as plt
  import weightedcalcs as weightLib


wc = weightLib.Calculator('weight')

hh = oio.readStage(
    cm.subsample
  , "households_2_purchases." + cm.strategy_year_suffix )

hh = hh[ ~ ( hh["income"].isnull()
           | hh["value, purchase"].isnull() ) ]

def months_to_save_for_a_month( income : float,
                                spending : float
                              ) -> float:
    return ( spending / (income - spending)
             if spending <= income
             else 1e4 )

hh["months to save for a month"] = hh.apply(
    lambda row: months_to_save_for_a_month(
        income = row["income"],
        spending = row["value, purchase"] ),
    axis = "columns" )

hh["months to save for a month, cash"] = hh.apply(
    lambda row: months_to_save_for_a_month(
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

def mk_samples( df : pd.DataFrame
              ) -> List[ Tuple[ str, pd.DataFrame ] ]:
  return [ ("full sample", df ),
           ("3 or more",   df[ df["members"] >= 3    ] ),
           ("female head", df[ df["female head"] > 0 ] ),
           ("has child",   df[ df["has-child"] > 0   ] ),
           ("has elderly", df[ df["has-elderly"] > 0 ] ) ]

def quantiles_report( samples : List[ Tuple[ str, pd.DataFrame ] ],
                      colname : str,
                      quantiles : List[float],
                      add_unity : bool = False
                    ) -> pd.DataFrame:
    sample_names = list( map( lambda pair: pair[0],
                              samples ) )
    qd = pd.DataFrame( # quantile data
        columns = sample_names,
        index = quantiles + ( [1] if add_unity else [] ) )
    for q in quantiles:
        for (name,sample) in samples:
            qd[name][q] = wc.quantile( sample,
                                       colname,
                                       q )
    return ( qd.applymap(
               # PITFALL: This handles the case of NaN correctly
               # because NaN < x is false for all x.
               lambda x: x if x < 9999 else np.inf )
            . transpose() . round(2) )

deciles = list( np.round(
    np.arange( 0.1, 1, 0.1 ),
    1 ) )

zoom_quantiles = list( np.round(
    np.arange( 0.32, 0.45001, 0.01 ),
    2 ) )

if True:
  assert cm.subsample == 1
  every = quantiles_report(
      mk_samples(
          # full sample gives just about identical results
          hh[ hh["recently bought this house"] <= 0 ] ),
      "months to save for a month, cash",
      deciles,
      add_unity = True )
  zoom = quantiles_report(
      mk_samples(
          # full sample gives just about identical results
          hh[ hh["recently bought this house"] <= 0 ] ),
      "months to save for a month, cash",
      zoom_quantiles )

# Including non-cash income would seem to compare apples and oranges,
# although the results are largely the same.
#
# every_ = quantiles_report(
#     mk_samples(
#         # full sample gives just about identical results
#         hh[ hh["recently bought this house"] <= 0 ] ),
#     "months to save for a month",
#     deciles,
#     add_unity = True )
#
# zoom_ = quantiles_report(
#     mk_samples(
#         # full sample gives just about identical results
#         hh[ hh["recently bought this house"] <= 0 ] ),
#     "months to save for a month",
#     zoom_quantiles )


############## How much money the extreme savers make ##############

q = wc.quantile( hh, # the top decile of savers
        "months to save for a month, cash",
        0.1 )

high_savers = hh[ hh[ "months to save for a month, cash" ] < q ]
s["income, cash"].describe()

for q in np.arange(0,1,0.05):
  print( round( q*100),
         round( wc.quantile( high_savers, "income, cash", q ) ) )

high_saving_poor = hh [   (hh[ "months to save for a month, cash" ] < q)
                        & (hh[ "income, cash" ] < 5e5) ]

# The poorest high-savers aren't surviving on in-kind income we know about.
# Nor are they receiving non-purchase goods sufficient to bring their
# incomes to something one might consider
( high_saving_poor
  [[ "income, in-kind", "value, non-purchase"]]
  . describe() )

