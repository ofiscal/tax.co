# PITFALL:
# Unlike the other "people_*" programs,
# this one does not contain everybody -- just earners.

# PURPOSE:
# From people, isolates earners.
# Computes each earner's share of total household income,
# and from there, attributes other consumption, spending and tax variables.
# Computes each earner's income quantile,
# various fractions of the variables so far described in this comment,
# and total tax (just called "tax").

# ABOUT THE NAME "post households":
# This merges the household-level output of households_2_purchases.py
# into the person-level output of people_3_income_taxish.py.
# It is therefore called "post households"
# because it runs after the "households_*" programs,
# unlike all the earlier people_* programs,
# which run before and are used by the households_* programs.

if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.output_io as oio
  import python.common.common as com
  import python.build.people_4_earners_post_households_defs as defs


if True: # input
  hs = oio.readUserData (
    com.subsample,
    "households_2_purchases." + com.strategy_year_suffix )
  ps = oio.readUserData (
    com.subsample,
    'people_3_income_taxish.' + com.strategy_year_suffix )

if True: # Prepare to merge.
  hs = hs.rename ( columns = {"income" : "income, household"} )

if True: # Merge people and households.
  m = pd.merge ( left = ps,
                 right = hs[ defs.columns_to_pull_from_hs ],
                 on = "household" )
  earners = m [ (   ( m [ "in labor force" ] == 1 )
                  & ( m [ "age" ] >= 18 ) )
                | (   m [ "income" ] > 2 ) ]
  del(m)

if True: # Make new variables, esp. create person-level purchase-like
  earners["share"] = np.where ( # The fraction of purchaselike variables
                                # attributed to this household adult.
    earners["income, household"] <= 200,               # the condition
      # PITFALL: Since some households are enormous and income is fuzzed,
      # total income for a household that earns nothing can be
      # much greater than 0. Hence the 100 where you might expect 0.
    1 / earners["members in labor force"],             # used if true
    earners["income"] / earners["income, household"] ) # used if false
  earners["one"] = 1 # To define the trivial group in the person-level report.
  for i in defs.household_variables_to_allocate_by_income_share:
    earners[i] = earners[i] * earners["share"]

if True: # more variables
  for label, n in [ ("income-decile"    , 10),
                    ("income-percentile", 100),
                    ("income-millile"   , 1000), ]:
    earners[label] = util.myQuantile (
      n_quantiles = n,
      in_col = earners["income"] )
  earners["vat / purchase value" ] = (
    earners["vat paid"] / earners["value, purchase" ] )
  earners["vat / income"] = (
    # PITFALL: While the maximum value of this looks absurd (103),
    # it's not. The 95th percentile is 0.3. The outliers are so high because
    # people can spend borrowed money.
    earners["vat paid"] / earners["income"] )
  earners["purchase value / income"] = (
    earners["value, purchase"] / earners["income"] )
  earners["tax"] = (
    # PITFALL: This must be computed separately for households and earners,
    # because income and ss taxes vary by earner.
    # (The VAT and other purchaselike taxes are, by contrast,
    # allocated within households based on each earner's income.)
    earners [ [ "tax, income",
                "tax, ss",
                "vat paid",
                "value, tax, purchaselike non-VAT" ] ]
    . sum ( axis = "columns" ) )

if True: # save
  oio.saveUserData (
    com.subsample,
    earners,
    "people_4_earners_post_households." + com.strategy_year_suffix )
