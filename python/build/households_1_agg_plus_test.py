if True:
  from typing import List
  import sys
  import pandas as pd
  #
  import python.build.classes                    as cl
  import python.build.households_1_agg_plus_defs as defs
  import python.build.output_io                  as oio
  import python.common.common                    as com
  import python.common.misc                      as misc
  import python.common.util                      as util


def test_const_within_group( gs : List[str],
                             cs : List[str],
                             d  : pd.DataFrame ) -> bool:
    """Tests that the columns `cs` are constant within each of the groups defined by `gs`."""
    h = d.groupby( gs )
    for c in cs:
        assert h[c].nunique().max() == 1

if True: # IO
  ppl = oio.readStage(
    com.subsample,
    "people_3_income_taxish." + com.strategy_year_suffix )
  hh = oio.readStage(
    com.subsample,
    "households_1_agg_plus." + com.strategy_year_suffix )
  test_const_within_group(
      # TODO ? move this test to the tests of person data
      ["household"],
      defs.cols_const_within_hh,
      hh )
  assert len(hh) == ppl["household"].nunique()

# old columns:
#   ? test that the summed vars' sums are very close to their means in the prev data
#     because this should not change upon aggregating from people to households
#
# new columns:
# income, rank 1-5
# income, labor, rank 1-5
#
# how to test the min, max columns?
#   age-min in the household data should have a mean that is substantially less than the mean for age in the person data, and stricly less than its max
#   generalize that
#
# how to test has-elderly, etc?
#   has-child should have a mean that is substantially more than the fraction of people under 18
#
# income-decile, income-percentile
#   test their ranges, min, max, mean
