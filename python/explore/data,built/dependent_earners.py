# ### Problem : Could claim a dependent and also be claimed?
# 
# Consider a household with 3 people, with 2 of them earners and 2 of them claimable as dependents.
# Currently the algorithm gives a dependent to both earners -- after all, there are two dependents to claim, and two earners to claim them.
# What should it do instead?
# 
# 
# ### Daniel: nobody can be claimed as a dependent and simultaneously claim one
# So do I have to compute the rational choice?
# 
# 
# ### things to use
# ppl = oio.readStage( com.subsample
#                    , "people_3_purchases." + com.strategy_suffix )
# people_4_income_taxish_functions . insert_has_dependent_column
#   pd.DataFrame -> pd.DataFrame
# people["dependent"]
# r2018 . income_taxes( ppl )
# 
# 
# ### how to test
# Restrict the file to dependents.
# Mark everyone as having a dependent.
# Compute everyone's taxes.
# Restrict to people with "tax, income" > 0.
# Is the set empty?

if True:
    import pandas as pd
    #
    import python.common.common      as com
    import python.build.output_io as oio
    import python.regime.r2018 as reg
    import python.build.ss_functions as ss

ppl = oio.readStage( com.subsample
                   , "people_3_purchases." + com.strategy_suffix )

if True:
  ppl = ppl[ ppl["dependent"] ]
  ppl = ss.mk_ss_contribs( ppl )
  ppl["has dependent"] = False
  ppl = reg.income_taxes( ppl )
  len( ppl[ ppl["tax, income"] > 0 ] )

rich_deps = ppl[ ppl["tax, income"] > 0 ].copy()
rich_deps["tax, income"].describe()
