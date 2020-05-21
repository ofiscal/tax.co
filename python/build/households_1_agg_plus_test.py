if True:
  from typing import List
  import sys
  import pandas as pd
  #
  import python.build.households_1_agg_plus_defs as defs
  import python.build.output_io                  as oio
  import python.common.common                    as com


def test_const_within_group( gs : List[str],
                             cs : List[str],
                             d  : pd.DataFrame ) -> ():
    """Tests that the columns `cs` are constant within each of the groups defined by `gs`."""
    h = d.groupby( gs )
    for c in cs:
        assert h[c].nunique().max() == 1

def test_indices( hh  : pd.DataFrame,
                  ppl : pd.DataFrame
                ) ->    ():
  assert len(hh) == ppl["household"].nunique()
  assert ( # verify that cols_all's components do not overlap
      len( defs.cols_all )
      == len( ["household"] )
      +  len( defs.cols_const_within_hh )
      +  len( defs.cols_most )
      +  len( defs.cols_to_min_or_max__no_name_change )
      +  len( defs.cols_to_min_or_max__post_rename )
      +  len( defs.cols_new ) )
  assert set( defs.cols_all ) == set( hh.columns )


if True: # IO
  log = "starting\n"
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
  test_indices( hh=hh, ppl=ppl )
  test_income_ranks(hh)

  oio.test_write(
      com.subsample,
      "households_1_agg_plus",
      log )


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
