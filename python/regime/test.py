if True:
  import pandas                as pd
  #
  from   python.common.misc import muvt
  import python.regime.strategy_dependent as strat_dep


def test_cgg_single_2052_UVT_income_tax_deduction ():
  df = pd.DataFrame (
    { "renta liquida" : [ i * muvt
                          for i in [0, 2000, 2100, 5000] ],
      "claims dependent (labor income tax)" : [False] * 4 } )
  res = df . apply (
    strat_dep.cgg_single_2052_UVT_income_tax_deduction,
    axis = 1 )
  should_be_small = (
    res
    - pd.Series (
      [ i * muvt
        for i in [ 0, 0, 2100 - 2052, 5000 - 2052] ] ) )
  assert should_be_small . abs() . max() < 1e-5
