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


if True: # choose one of these, or write another
  if True:
    drop_used_savings = True # whether to drop households that used savings
    income = ( # choose one
        # "income, cash"
        "ICMD"
        )
    spending = ( # choose one
        # "value, purchase"
        "GCM"
        )
  if False:
    drop_used_savings = False
    income = "ICMD"
    spending = "GCM"
    zoom_min = 0.48
    zoom_max = 0.65

sink = open( ( "output/time_to_save/" +
               str(cm.subsample) + ":" +
               str(drop_used_savings) +
               income + ":" +
               spending + ".txt" ),
             "w")
pd.options.display.width = 5555
pd.options.display.max_columns = 5555

wc = weightLib.Calculator('weight')

hh = oio.readStage(
    cm.subsample
  , "households_2_purchases." + cm.strategy_year_suffix )

hh = hh[ ~ ( hh[income].isnull()
           | hh[spending].isnull() ) ]

sink.write( "\n".join( [
    "hh.dtypes",
    str( hh[[income,spending]]
         .dtypes ),
    "\n" ] ) )

hh["months to save for a month"] = hh.apply(
    lambda row: defs.months_to_save_for_a_month(
        income = row[income],
        spending = row[spending] ),
    axis = "columns" )

if True: # explore
  sink.write( "\n".join( [
    "months to save for a month",
    str( hh["months to save for a month"].describe() ),
    "\nused savings",
    str( hh["used savings"].astype(int).describe() ),
    "\nrecently bought this house",
    str( hh["recently bought this house"].astype(int).describe() ),
    #
    "\nlen(hh)" ,
    str( len(hh) ),
    "\nlen( hh[ hh[\"used savings\"] > 0 ] )" ,
    str( len( hh[ hh["used savings"] > 0 ] ) ),
    "\nlen( hh[ hh[\"recently bought this house\"] > 0 ] )" ,
    str( len( hh[ hh["recently bought this house"] > 0 ] ) ),
    "\nlen( hh[ hh[\"used savings\"] > 0 ] ) / len(hh)" ,
    str( len( hh[ hh["used savings"] > 0 ] ) / len(hh) ),
    "\n\n"
    ] ) )

if drop_used_savings:
  hh = hh[ hh["used savings"] <= 0 ]
  # hh = hh.drop( columns = ["used savings"] )

deciles = list( np.round(
    np.arange( 0.1, 1, 0.1 ),
    1 ) )

zoom_quantiles = list( np.round(
    np.arange( zoom_min, zoom_max, 0.01 ),
    2 ) )

if True:
  assert cm.subsample < 5
  every = defs.quantiles_report(
      defs.mk_samples(
          # full sample gives just about identical results
          hh[ hh["recently bought this house"] <= 0 ] ),
      "months to save for a month",
      wc,
      deciles,
      add_unity = True )
  zoom = defs.quantiles_report(
      defs.mk_samples(
          # full sample gives just about identical results
          hh[ hh["recently bought this house"] <= 0 ] ),
      "months to save for a month",
      wc,
      zoom_quantiles )

sink.write( "\n".join( [
    "every decile",
    str(every),
    "\nzooming in on the percentiles where people become unable to save",
    str(zoom),
    "\n\n"
    ] ) )


############## How much money the extreme savers make ##############

q = wc.quantile( hh, # the top decile of savers
        "months to save for a month",
        0.1 )

high_savers = hh[ hh[ "months to save for a month" ] < q ]

sink.write( "\n".join(
  [ "high savers' income",
    str( high_savers[income].describe() ),
    "\n\n",
    "high saver income quantiles:"
    ] ) )

for q in np.arange(0,1,0.05):
  sink.write(
    str( round( q*100) ) + ": " +
    str( round( wc.quantile( high_savers, income, q ) ) ) +
    "\n" )

sink.write( "\n\n" )

high_saving_poor = hh [
     (hh[ "months to save for a month" ] < q) &
     (hh[ income ] < 5e5) ]

# The poorest high-savers aren't surviving on in-kind income we know about.
# Nor are they receiving non-purchase goods sufficient to bring their
# incomes to something one might consider
sink.write(
    "high-saving poor: " +
    str( high_saving_poor
         [[ "income, in-kind", "value, non-purchase"]]
         . describe() ) +
    "\n\n" )

sink.close()

