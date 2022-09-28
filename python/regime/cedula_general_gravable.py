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
      terms. reduce_income_tax_deduction_to_1210_uvts
      : cgg_reduce_income_tax_deduction_to_1210_uvts,
      terms.detail
      : cgg_detail }
    [ com.strategy ] # lookup a function from the dictionary
    ( row ) )        # apply an argument to the function

def cgg_detail ( row: pd.Series ) -> float:
  """
  `stage_1` is someone's income,
  minus either 32.5% or 5040 UVTs, whichever is smaller.
  If someone cannot claim dependents,
  then the second stage equals the first.
  If they can, then the second stage is equal to
  stage_1 minus 10% or 32 UVT, whichever is smaller.
  The second stage is the function's return value.
  """
  stage_1 = max ( ( row                 ["renta liquida"]
                    - min ( 0.325 * row ["renta liquida"],
                            5040 * muvt ) ),
                  0 )
  return ( stage_1
           if   not row["claims dependent (labor income tax)"]
           else stage_1 - min ( 0.1 * stage_1,
                                32 * muvt ) )

def cgg_reduce_income_tax_deduction_to_1210_uvts ( row: pd.Series ) -> float:
  stage_1 = max ( ( row                 ["renta liquida"]
                    - min ( 0.325 * row ["renta liquida"],
                            1210 * muvt ) ),
                  0 )
  return ( stage_1
           if   not row["claims dependent (labor income tax)"]
           else stage_1 - min ( 0.1 * stage_1,
                                32 * muvt ) )

def cgg_single_cedula_with_single_1210_uvt_threshold (
    row: pd.Series
) -> float:
  stage_1 = max ( ( row                ["renta liquida"]
                    - min( 0.325 * row ["renta liquida"],
                           1210 * muvt ) ),
                  0 )
  return ( stage_1
           if   not row ["claims dependent (labor income tax)"]
           else stage_1 - min ( 0.1 * stage_1,
                                32 * muvt ) )
