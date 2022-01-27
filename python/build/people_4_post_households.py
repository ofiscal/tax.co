if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.output_io as oio
  import python.common.common as com


if True: # input
  hs = oio.readStage (
    com.subsample,
    "households_2_purchases." + com.strategy_year_suffix )
  ps = oio.readStage (
    com.subsample,
    'people_3_income_taxish.' + com.strategy_year_suffix )

if True: # Prepare to merge.
  hs = hs.rename ( columns = {"income" : "income, household"} )
  household_variables_to_allocate_by_income_share = [
    "value, consumption",
    "value, non-purchase",
    "value, purchase",
    "value, spending",
    "value, tax, predial",
    "value, tax, purchaselike non-predial non-VAT",
    "value, tax, purchaselike non-VAT",
    "vat paid",
    ]
  columns_to_pull_from_hs = ( [
    "household",
    "adults",            # Number of household members >= 18.
    "income, household", # For allocating VAT among household members
                         # according to each member's income share.
    ] + household_variables_to_allocate_by_income_share )
  assert (
    set.intersection (
      set ( ps.columns ),
      set ( columns_to_pull_from_hs ) )
    == set ( ["household"] # PITFALL: If "household" isn't wrapped in a list, the result is a set of letters rather than a set containing a single word.
            ) )

if True: # Merge people and households.
         # Make new variables, esp. create person-level purchase-like
  m = pd.merge ( left = ps,
                 right = hs[ columns_to_pull_from_hs ],
                 on = "household" )
  earners = m [ m["income"] > 0 ]  # TODO: This should also include
                                   # adults in the labor force.
  del(m)
  earners["share"] = np.where ( # The fraction of purchaselike variables
                                # attributed to this household adult.
    earners["income, household"] <= 0,          # the condition
    1 / earners["adults"],                      # used if true
    earners["income"] / earners["income, household"] ) # used if false
  earners["one"] = 1 # To define the trivial group in the person-level report.
  for i in household_variables_to_allocate_by_income_share:
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
  earners["purchase value / income"   ] = (
    earners["value, purchase"] / earners["income"] )
