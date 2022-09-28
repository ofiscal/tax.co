if True:
  import pandas                as pd
  #
  import python.common.common  as com
  from   python.common.misc import muvt
  import python.common.terms   as terms


### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Ways to compute the cedula general gravable
### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def cedula_general_gravable ( row: pd.Series ) -> float:
  return (
    { terms. single_cedula_with_single_1210_uvt_threshold
      : cgg_single_cedula_with_single_1210_uvt_threshold,
      terms. single_1210_UVT_income_tax_deduction
      : cgg_single_1210_UVT_income_tax_deduction,
      terms.detail
      : cgg_detail }
    [ com.strategy ] # lookup a function from the dictionary
    ( row ) )        # apply an argument to the function

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
  s1 = max ( ( row                 ["renta liquida"]
               - min ( 0.325 * row ["renta liquida"],
                       5040 * muvt ) ),
             0 )
  return ( s1
           if   not row["claims dependent (labor income tax)"]
           else s1 - min ( 0.1 * s1,
                           32 * muvt ) )

def cgg_single_1210_UVT_income_tax_deduction ( row: pd.Series ) -> float:
  stage1 = max ( row ["renta liquida"] - 1210 * muvt,
                 0 )
  return ( stage1
           if not row["claims dependent (labor income tax)"]
           else  stage1 - min( 0.1 * stage1,
                               32 * muvt ) )

def cgg_single_cedula_with_single_1210_uvt_threshold (
    row: pd.Series
) -> float:
  s1 = max ( ( row                ["renta liquida"]
               - min( 0.325 * row ["renta liquida"],
                      1210 * muvt ) ),
             0 )
  return ( s1
           if   not row ["claims dependent (labor income tax)"]
           else s1 - min ( 0.1 * s1,
                           32 * muvt ) )
