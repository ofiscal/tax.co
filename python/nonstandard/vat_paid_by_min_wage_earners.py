# PURPOSE: This computes the average VAT paid
# by people making near the minimum wage.

if True:
  import numpy                   as np
  import os
  import pandas                  as pd
  #
  import python.build.output_io  as oio
  import python.common.common    as com
  import python.common.describe  as desc
  import python.common.misc      as c
  import python.common.util      as util
  from   python.common.misc import min_wage


##################################
### Load, futz with input data ###
##################################

### TODO | PITFALL: This section is entirely duplicative,
### as of Fri Sep 16 2022,
### of the similarly-named section in python.build.var_summaries_by_group.
### It should be factored out into a separate part of the Makefile.


if True: # load data
  households = oio.readUserData(
      com.subsample,
      "households_2_purchases." + com.strategy_year_suffix )

  earners = oio.readUserData(
      com.subsample,
      "people_4_post_households." + com.strategy_year_suffix )

if True: # generate "income - tax"
  for df in (households, earners):
    df["income - tax"] = df["income"] - df["tax"]

if True: # nonzero labor income earners
  nonzero_laborers = earners.copy()
  nonzero_laborers = nonzero_laborers [
    # PITFALL: Since a random amount between 0 and 1 peso
    # is added to labor income in `build.people.main`
    # (in order to make the quantiles all the same size),
    # this keeps only people with income greater than 2 pesos,
    # rather than people with any nonzero labor income.
    nonzero_laborers ["income, labor"] > 2 ]
  for label, n in [ ("income-decile"    , 10),
                    ("income-percentile", 100),
                    ("income-millile"   , 1000), ]:
    nonzero_laborers[label] = (
      util.myQuantile (
        n_quantiles = n,
        in_col = nonzero_laborers["income, labor"] )
      . astype ( int ) )

if True: # Create a few columns missing in the input data.
         # TODO ? Move upstream.
  for df in [households, earners, nonzero_laborers]:
    df["income, labor + cesantia"] = (
        df["income, labor"]
        + df["income, cesantia"] )

    df["income-percentile-in[90,97]"] = (
        (df["income-percentile"] >= 90)
      & (df["income-percentile"] <= 97) )

    df["income-percentile-in[90,98]"] = (
        (df["income-percentile"] >= 90)
      & (df["income-percentile"] <= 98) )

    df["income-millile-in[990,997]"] = (
        (df["income-millile"] >= 990)
      & (df["income-millile"] <= 997) )

    df["income-millile-in[990,998]"] = (
        (df["income-millile"] >= 990)
      & (df["income-millile"] <= 998) )

    df["income < min wage"] = (
      df["income"] < c.min_wage )

if True: # Make some subsets.
  # PITFALL: All changes to `earners`, `households` should precede this.
  householdsFemale = households[ households["female head"] == 1 ] . copy()
  householdsMale   = households[ households["female head"] == 0 ] . copy()
  earnersFemale = earners[ earners["female"] == 1 ] . copy()
  earnersMale   = earners[ earners["female"] == 0 ] . copy()


#########################
### Compute the thing ###
#########################

print()
print ( "All of the following figures are denominated in peso values recorded in the ENPH, i.e. as of sometime between July 2016 and June 2017. They have not been adjusted for inflation." )
print()
print ( "The average minimum wage in 2016 and 2017 was " + str(min_wage) + ". (That's a simple arithmetic mean, but the logarithmic mean is equal to the arithmetic one to three decimal places.)" )

for radius in [0.1, 1]:
  for (label, superset) in [ ("Male", earnersMale),
                             ("Female", earnersFemale) ]:
    subset = superset [
      ( superset [ "income" ] < (min_wage * (1 + radius/100) ) ) &
      ( superset [ "income" ] > (min_wage * (1 - radius/100) ) ) ]
    vat_paid = subset [ "vat paid" ] . mean ()
    sample_size = len ( subset )
    print()
    print ( label + " earers whose total (not just labor) income was within " + str(radius) + "% of the minimum wage in those years paid " + str ( vat_paid ) + " VAT per month on average. The sample contains " + str ( sample_size ) + " such people." )
