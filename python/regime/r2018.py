import pandas as pd
from python.common.misc import muvt


income_tax_columns = [ "tax, income"
                     , "tax, income, most"
                     , "tax, income, dividend"
                     , "tax, income, inheritance"
                     ]

gravable_pre = "cedula general gravable, sums before exemptions"

def non_dividend_income_tax( income : float ) -> float:
  # see test/income_tax_2018.hs for code that generates these formulas.
  # Run this to test the accumulated totals
  # (the numbers just after the + signs):
  #   ns = [ 0.19 * (1700 - 1090),
  #        0.28 * (4100 - 1700),
  #        0.33 * (8670 - 4100),
  #        0.35 * (18970 - 8670),
  #        0.37 * (31000 - 18970) ]
  #   for i in range(0,5):
  #     print( sum( ns[0:i+1] ) )

  x = income
  return (
    0                                           if x < ( 1090*muvt)
    else ( (x -  1090 * muvt)*0.19              if x < ( 1700*muvt)
    else ( (x -  1700 * muvt)*0.28 +   116*muvt if x < ( 4100*muvt)
    else ( (x -  4100 * muvt)*0.33 +   788*muvt if x < ( 8670*muvt)
    else ( (x -  8670 * muvt)*0.35 +  2296*muvt if x < (18970*muvt)
    else ( (x - 18970 * muvt)*0.39 +  5901*muvt if x < (27595*muvt)
    else ( (x - 27595 * muvt)*0.44 +  9265*muvt if x < (36000*muvt)
    else ( (x - 36000 * muvt)*0.47 + 12963*muvt if x < (55000*muvt)
    else ( (x - 55000 * muvt)*0.5  + 21893*muvt if x < (90000*muvt)
    else ( (x - 90000 * muvt)*0.55 + 39393*muvt
          ) ) ) ) ) ) ) ) ) )

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
    row               [gravable_pre]
    - min( 0.325 * row[gravable_pre],
           5040 * muvt ) )
  s2 = ( s1 if not row["has dependent"]
         else  s1 - min( 0.1 * s1,
                         32 * muvt ) )
  return s2

def income_taxes( ppl : pd.DataFrame ) -> pd.DataFrame:
  """PITFALL: Destructive."""
  new_columns = pd.DataFrame()
  temp_columns = pd.DataFrame()
  temp_columns["has dependent"] = ppl["has dependent"]
  temp_columns[gravable_pre] = (
    ( ( ppl["income, labor"]
      - ppl["tax, ss, total employee contribs"] )
    + ppl["income, capital (tax def)"]
    + ppl["income, non-labor"]
    ) )

  temp_columns["cedula general gravable"] = (
    temp_columns .
    apply(taxable, axis=1) )

  new_columns["tax, income, most"] = (
    temp_columns["cedula general gravable"] +
    ppl["income, pension"]
  ) . apply( non_dividend_income_tax )

  new_columns["tax, income, dividend"] = (
    ppl["income, dividend"].apply( lambda x:
      0 if x < (300*muvt)
      else (x - 300*muvt) * 0.15 ) )

  new_columns["tax, income, inheritance"] = (
    ppl["income, inheritance"].apply( lambda x:
      0 if x < (112337*muvt)
      else (   (x -  112337 * muvt)*0.1                if x < ( 280884*muvt)
        else ( (x -  280884 * muvt)*0.2 +   16855*muvt if x < (2808436*muvt)
          else (x - 2808436 * muvt)*0.33 + 522365*muvt
          ) ) ) )

  new_columns["tax, income"] = (
    new_columns["tax, income, most"] +
    new_columns["tax, income, dividend"] +
    new_columns["tax, income, inheritance"]
    )

  return pd.concat( [ppl, new_columns], axis = 1 )

