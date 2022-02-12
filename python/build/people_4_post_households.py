if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.output_io as oio
  import python.common.common as com
  import python.build.people_4_post_households_defs as defs


if True: # input
  hs = oio.readStage (
    com.subsample,
    "households_2_purchases." + com.strategy_year_suffix )
  ps = oio.readStage (
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
                | (   m [ "income" ] > 0 ) ]
  del(m)

if True: # Make new variables, esp. create person-level purchase-like
  earners["share"] = np.where ( # The fraction of purchaselike variables
                                # attributed to this household adult.
    earners["income, household"] <= 0,                 # the condition
    1 / earners["members in labor force"],             # used if true
    earners["income"] / earners["income, household"] ) # used if false
  earners["one"] = 1 # To define the trivial group in the person-level report.
  for i in defs.household_variables_to_allocate_by_income_share:
    earners[i] = earners[i] * earners["share"]

if True: # more variables
  earners["income-decile"] = (
    util.noisyQuantile( 10, 0, 1, earners["income"] ) )
  earners["income-percentile"] = (
    util.noisyQuantile( 100, 0, 1, earners["income"] ) )
  earners["vat / purchase value" ] = (
    earners["vat paid"]   / earners["value, purchase" ] )
  earners["vat/income"] = (
    # PITFALL: While the maximum value of this looks absurd (103),
    # it's not. The 95th percentile is 0.3. The outliers are so high because
    # people can spend borrowed money.
    earners["vat paid"]   / earners["income"] )
  earners["purchase value / income"] = (
    earners["value, purchase"] / earners["income"] )

if True: # save
  oio.saveStage(
      com.subsample,
      earners,
      "people_4_post_households." + com.strategy_year_suffix )
