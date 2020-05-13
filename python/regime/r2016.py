import pandas as pd
from python.common.misc import muvt


income_tax_columns = [ "tax, income"
                     , "tax, income, labor + pension"
                     , "tax, income, capital + non-labor"
                     , "tax, income, dividend"
                     ]

def income_taxes( ppl ):
  """Add income tax columns to ppl.
PITFALL: The exemption for earners claiming dependents is not implemented."""
  new_columns = pd.DataFrame()
  temp_columns = pd.DataFrame()
  temp_columns["taxable income, labor + pension"] = (
    ( ppl["income, pension"]
    + ( ppl["income, labor"]
      - ppl["tax, ss, total employee contribs"] )
    ).apply( lambda x: x - min( 0.325 * x, 5040 * muvt) )
  )
  new_columns["tax, income, labor + pension"] = (
    temp_columns["taxable income, labor + pension"].apply( lambda x:
                    0                          if x < (1090*muvt)
      else (   (x - 1090*muvt)*0.19            if x < (1700*muvt)
        else ( (x - 1700*muvt)*0.28 + 116*muvt if x < (4100*muvt)
          else (x - 4100*muvt)*0.33 + 788*muvt ) ) ) )

  temp_columns["taxable income, capital"] = (
    ppl["income, capital (tax def)"].apply(
      lambda x: x - min( 0.1 * x, 1000*muvt)
    ) )
  temp_columns["taxable income, non-labor"] = (
    ppl["income, non-labor"].apply(
      lambda x: x - min( 0.1 * x, 1000*muvt)
    ) )

  new_columns["tax, income, capital + non-labor"] = (
    ( temp_columns["taxable income, capital"]
    + temp_columns["taxable income, non-labor"]
    ).apply( lambda x:
                     0                               if x < ( 600*muvt)
        else (       (x - 600 *muvt)*0.1             if x < (1000*muvt)
          else (     (x - 1000*muvt)*0.2  + 40 *muvt if x < (2000*muvt)
            else (   (x - 2000*muvt)*0.3  + 240*muvt if x < (3000*muvt)
              else ( (x - 3000*muvt)*0.35 + 540*muvt if x < (4000*muvt)
                else (x - 4000*muvt)*0.4  + 870*muvt ) ) ) ) ) )

  new_columns["tax, income, dividend"] = (
    ppl["income, dividend"].apply( lambda x:
             0                      if x < ( 600*muvt)
      else ( (x -  600*muvt) * 0.05 if x < (1000*muvt)
        else (x - 1000*muvt) * 0.1 + 20*muvt ) ) )
  new_columns["tax, income"] = (
    new_columns.sum( axis = 1 ) )

  return pd.concat( [ppl, new_columns], axis = 1 )
