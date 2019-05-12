import pandas as pd
from python.common.misc import muvt

income_tax_columns = [ "tax, income"
                     , "tax, income, all but dividend"
                     , "tax, income, dividend"
                     ]

def income_taxes( ppl ):
  new_columns = pd.DataFrame()
  temp_columns = pd.DataFrame()
  temp_columns["cedula general gravable"] = (
    ( ppl["income, labor"] +
      ppl["income, capital (tax def)"] +
      ppl["income, non-labor"]
    ) . apply( lambda x: x - min( 0.325 * x
                                , 5040 * muvt ) ) )

  new_columns["tax, income, all but dividend"] = (
    temp_columns["cedula general gravable"] +
    ppl["income, pension"]
  ) . apply( lambda x:
    # see test/income_tax_2018.hs for code that generates these formulas
                        0                               if x < (1090 *muvt)
    else (         (x - 1090 *muvt)*0.19                if x < (1700 *muvt)
      else (       (x - 1700 *muvt)*0.28 + 115.9  *muvt if x < (4100 *muvt)
        else (     (x - 4100 *muvt)*0.33 + 787.9  *muvt if x < (8670 *muvt)
          else (   (x - 8670 *muvt)*0.35 + 2296   *muvt if x < (18970*muvt)
            else ( (x - 18970*muvt)*0.37 + 5901   *muvt if x < (31000*muvt)
              else (x - 31000*muvt)*0.39 + 10352.1*muvt
                  ) ) ) ) ) )

  new_columns["tax, income, dividend"] = (
    ppl["income, dividend"].apply( lambda x:
      0 if x < (300*muvt)
      else (x - 300*muvt) * 0.15 ) )
  new_columns["tax, income"] = (
    new_columns["tax, income, all but dividend"] +
    new_columns["tax, income, dividend"] )

  return pd.concat( [ppl, new_columns], axis = 1 )
