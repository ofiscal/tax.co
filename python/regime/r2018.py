import pandas as pd
from python.common.misc import muvt


income_tax_columns = [ "tax, income"
                     , "tax, income, all but dividend"
                     , "tax, income, dividend"
                     ]

def taxable( row: pd.Series ) -> float:
  """
  The first stage of "renta gravable laboral" is someone's income,
  minus either 32.5% or 5040 UVTs, whichever is smaller.
  If someone can claim no dependents, then their second stage renta gravable
  is the same as the first.
  If they can, and S1 is the value of the first stage,
  then the second stage is equal to S1 minus 10% or 32 UVT,
  whichever is smaller.
  """
  s1 = (
    row["cedula general gravable, sums before exemptions"]
    - min( 0.325 * row["cedula general gravable, sums before exemptions"],
           5040 * muvt ) )
  s2 = ( s1 if not row["has dependent"]
         else  s1 - min( 0.1 * s1,
                         32 * muvt ) )
  return s2

def income_taxes( ppl ):
  new_columns = pd.DataFrame()
  temp_columns = pd.DataFrame()
  temp_columns["has dependent"] = ppl["has dependent"]
  temp_columns["cedula general gravable, sums before exemptions"] = (
    ( ( ppl["income, labor"]
      - ppl["tax, ss, total employee contribs"] )
    + ppl["income, capital (tax def)"]
    + ppl["income, non-labor"]
    ) )
  temp_columns["cedula general gravable"] = (
    temp_columns .
    apply(taxable, axis=1) )

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
