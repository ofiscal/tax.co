if True:
  import pandas                as pd
  #
  from   python.common.misc import muvt


### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Some algorithms to compute the cedula general gravable
### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def cgg_detail ( row: pd.Series ) -> float:
  """
  The first stage, "s1", is someone's income,
  minus either 32.5% or 5040 UVTs, whichever is smaller.
  If someone cannot claim dependents,
  then the second stage equals the first.
  If they can, then the second stage is equal to
  s1 minus 10% or 32 UVT, whichever is smaller.
  The second stage is the function's return value.
  """
  s1 = ( row                ["renta liquida"]
         - min( 0.325 * row ["renta liquida"],
                5040 * muvt ) )
  return ( s1
           if   not row["claims dependent (labor income tax)"]
           else s1 - min ( 0.1 * s1,
                           32 * muvt ) )

def cgg_single_2052_UVT_income_tax_deduction ( row: pd.Series ) -> float:
  stage1 = max ( row ["renta liquida"] - 2052 * muvt,
                 0 )
  return ( stage1
           if not row["claims dependent (labor income tax)"]
           else  stage1 - min( 0.1 * stage1,
                               32 * muvt ) )
