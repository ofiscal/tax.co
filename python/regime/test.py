if True:
  import pandas                as pd
  #
  from   python.common.misc import muvt
  import python.regime.cedula_general_gravable as cgg


def test_cgg_single_1210_UVT_income_tax_deduction ():
  df = pd.DataFrame (
    { "renta liquida" : [ i * muvt
                          for i in [0, 1200, 1220, 5000] ],
      "claims dependent (labor income tax)" : [False] * 4 } )
  res = df . apply (
    cgg.cgg_single_1210_UVT_income_tax_deduction,
    axis = 1 )
  should_be_small = (
    res
    - pd.Series (
      [ i * muvt
        for i in [ 0, 0, 1220 - 1210, 5000 - 1210] ] ) )
  assert should_be_small . abs() . max() < 1e-5
