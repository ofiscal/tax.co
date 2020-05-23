if True:
  from typing import List
  import sys
  import pandas as pd
  #
  import python.build.households_1_agg_plus_defs as defs
  import python.build.output_io                  as oio
  from   python.build.people.files import edu_key
  import python.common.common                    as com
  import python.common.util                      as util


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
           len(            defs.cols_all ) ==
           len( pd.Series( defs.cols_all ) . unique() ) )
  assert set( defs.cols_all ) == set( hh.columns )

def test_income_ranks( hh : pd.DataFrame,
                       ppl : pd.DataFrame ) -> ():
    ppl_cols = ["income", "income, labor"]
    for c in ppl_cols:
        def cr(n): return c + ", rank " + str(n)

        # The maximum earner earns what the maximum top earner earns.
        assert ppl[c].max() == hh[cr(1)].max()

        # Store these once to avoid repeatedly calculating them.
        hh_means = {}
        for n in range(1,6):
            hh_means[n] = hh[cr(n)] . mean()

        for n in range(1,6):
            # Even the average 5th-ranked earner makes more than this.
            assert ( hh_means[n] >=
                     ( # In the 1/1000 sample, no rank-5 earner makes money.
                       0 if ( (com.subsample == 1000) &
                              (n == 5) )
                       else 1000 ) )
            # Even among top-earners, some earn nothing.
            assert hh[cr(n)] . min() == 0

        for n in range(1,5):
            # Income ranks are ordered correctly.
            assert hh_means[n] > 2 * hh_means[n+1]

def test_sums( hh : pd.DataFrame,
               ppl : pd.DataFrame ) -> ():
    # test hh["members"]
    assert   hh["members"] . min() == 1
    assert ( hh["members"]           . max() ==
             ppl["household-member"] . max() )
    hh_members_mean = hh["members"].mean()
    assert ( (hh_members_mean > 2) &
             (hh_members_mean < 4) )

    assert ( ( hh [defs.income_and_tax] . sum() -
               ppl[defs.income_and_tax] . sum() )
             . abs() . max() ) < 1e-4

def test_extrema( hh : pd.DataFrame,
                  ppl : pd.DataFrame ) -> ():
    bool_cols = ( defs.cols_to_min_or_max__no_name_change +
                  [ "has-male",
                    "has-lit",
                    "has-student",
                    "has-female",
                    "has-indig",
                    "has-git|rom",
                    "has-raizal",
                    "has-palenq",
                    "has-whi|mest",
                    "has-child",
                    "has-elderly" ] )
    if com.subsample != 1000:
        for c in bool_cols:
            assert hh[c].min() == 0
            assert hh[c].max() == 1
        for c in ["age","edu"]:
            assert hh[c + "-max"].max() == ppl[c].max()

def test_quantiles( hh : pd.DataFrame ) -> ():
    for (col,top) in [ ("income-decile",10),
                       ("income-percentile",100) ]:
        assert hh[col].min() == 0
        assert hh[col].max() == top - 1
        if com.subsample != 1000:
            assert hh[col].mean() == (top - 1) / 2

if True: # IO
  log = "starting\n"
  #
  ppl = oio.readStage(
    com.subsample,
    "people_3_income_taxish." + com.strategy_year_suffix )
  hh = oio.readStage(
    com.subsample,
    "households_1_agg_plus." + com.strategy_year_suffix )
  #
  ppl["edu"] = util.interpretCategorical(
    ppl["edu"],
    edu_key.values() )

  test_const_within_group(
      # TODO ? move this test to the tests of person data
      gs = ["household"],
      cs = defs.cols_const_within_hh,
      d = hh )
  test_indices      ( hh=hh, ppl=ppl )
  test_income_ranks ( hh=hh, ppl=ppl )
  test_sums         ( hh=hh, ppl=ppl )
  test_extrema      ( hh=hh, ppl=ppl )
  test_quantiles( hh )

  oio.test_write(
      com.subsample,
      "households_1_agg_plus",
      log )


# how to test the min, max columns?
#   age-min in the household data should have a mean that is substantially less than the mean for age in the person data, and stricly less than its max
#   generalize that
#
# how to test has-elderly, etc?
#   has-child should have a mean that is substantially more than the fraction of people under 18
#
# income-decile, income-percentile
#   test their ranges, min, max, mean
