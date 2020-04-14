if True:
  import pandas as pd
  from python.common.util import near
  from python.common.misc import muvt
  import python.regime.r2018 as reg

if True: # For low earners (100 muvt is around 250K pesos / month)
  # and you have no dependents, 32.5% of your income is exempted
  r = pd.Series( { "has dependent" : False,
                   reg.gravable_pre : 100 * muvt } )
  assert near( reg.taxable(r),
               r[reg.gravable_pre] * (1 - 0.325) )
  # The dependent exemption knocks off 10% from what's left.
  r["has dependent"] = True
  assert near( reg.taxable(r),
               r[reg.gravable_pre] * (1 - 0.325) * 0.9 )

if True: # For high earners (20000 muvt is around 50 million / month)
  # and you have no dependents, 5040 muvt is exempted.
  r = pd.Series( { "has dependent" : False,
                   reg.gravable_pre : 20000 * muvt } )
  assert near( reg.taxable(r),
               r[reg.gravable_pre] - 5040 * muvt )
  # The dependent exemption knocks off another 32 muvt.
  r["has dependent"] = True
  assert near( reg.taxable(r),
               r[reg.gravable_pre] - 5072 * muvt )

