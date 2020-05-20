if True:
  import sys
  import pandas as pd
  #
  import python.build.classes   as cl
  import python.build.output_io as oio
  import python.common.common   as com
  import python.common.misc     as misc
  import python.common.util     as util


move some column set definitions to a _defs data set
  so that it can be used in tests, too

ppl = oio.readStage(
  c.subsample,
  "people_3_income_taxish." + com.strategy_year_suffix )
hh = oio.saveStage(
  c.subsample,
  households,
  "households_1_agg_plus." + com.strategy_year_suffix )

test that "region-1", "region-2", "estrato", "weight" are constant within household
  TODO ? move this test to the person data

old columns:
  ? test that the summed vars' sums are very close to their means in the prev data
    because this should not change upon aggregating from people to households

new columns:
income, rank 1-5
income, labor, rank 1-5

how to test the min, max columns?
  age-min in the household data should have a mean that is substantially less than the mean for age in the person data, and stricly less than its max
  generalize that
  
how to test has-elderly, etc?
  has-child should have a mean that is substantially more than the fraction of people under 18

income-decile, income-percentile
  test their ranges, min, max, mean

