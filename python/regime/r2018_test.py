if True:
  import datetime
  import pandas as pd
  #
  from   python.common.misc import muvt
  from   python.common.util import near
  import python.build.output_io as oio
  import python.common.common   as common
  import python.regime.r2018    as reg


def test_most_income_tax():
  f = reg.most_income_tax
  assert near( f( 500 * muvt ), 0 )
  x = 1500 * muvt
  assert near( f(x),
               (x - 1090 *muvt)*0.19 )
  x = 5e4 * muvt
  assert near( f(x),
               (x - 31000*muvt)*0.39 + 10352.1*muvt)

def test_taxable():
  if True: # For low earners (100 muvt is around 250K pesos / month)
    # and you have no dependents, 32.5% of your income is exempted
    r = pd.Series( { "claims dependent (labor income tax)" : False,
                     reg.gravable_pre : 100 * muvt } )
    assert near( reg.taxable(r),
                 r[reg.gravable_pre] * (1 - 0.325) )
    # The dependent exemption knocks off 10% from what's left.
    r["claims dependent (labor income tax)"] = True
    assert near( reg.taxable(r),
                 r[reg.gravable_pre] * (1 - 0.325) * 0.9 )

  if True: # For high earners (20000 muvt is around 50 million / month)
    # and you have no dependents, 5040 muvt is exempted.
    r = pd.Series( { "claims dependent (labor income tax)" : False,
                     reg.gravable_pre : 20000 * muvt } )
    assert near( reg.taxable(r),
                 r[reg.gravable_pre] - 5040 * muvt )
    # The dependent exemption knocks off another 32 muvt.
    r["claims dependent (labor income tax)"] = True
    assert near( reg.taxable(r),
                 r[reg.gravable_pre] - 5072 * muvt )
  
if True:
  test_most_income_tax()
  test_taxable()
  log = str( datetime.datetime.now() )
  for ss in common.valid_subsamples:
    # PITFALL: Looping over subsample sizes because this program
    # uses no data.
    # If it works, it works for all subsamples.
    oio.test_write( ss
                  , "regime_r2018"
                  , log )

