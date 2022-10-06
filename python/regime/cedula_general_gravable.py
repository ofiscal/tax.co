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
    { terms.single_cedula_with_single_1210_uvt_threshold
      : cgg_single_cedula_with_single_1210_uvt_threshold,
      terms.reduce_income_tax_deduction_to_1210_uvts
      : cgg_reduce_income_tax_deduction_to_1210_uvts,
      terms.max_1340_uvt_deduction_and_max_4_dependents_72_uvt_each
      : cgg_max_1340_uvt_deduction_and_max_4_dependents_72_uvt_each,
      terms.detail
      : cgg_detail }
    [ com.strategy ] # lookup a function from the dictionary
    ( row ) )        # apply an argument to the function

def cgg_detail ( row: pd.Series ) -> float:
  """
  You can't deduct more than 5040 UVTs.
  You can deduct somewhere between 25% and 40%,
  and we don't know what you'll arrive at, so we assume the average, 32.5%.
  After that you can deduct an additional 10% of what's left,
  or 32 UVTs, whichever is smaller.
  """
  a1 = row ["renta liquida"] - 5040 * muvt
  x  = row ["renta liquida"] * (1 - 0.325)
  a2 = ( x
         if   not row["claims dependent (labor income tax)"]
         else x - min ( 0.1 * x,
                        32 * muvt ) )
  return max ( 0, a1, a2 )

# Being considered in Congress as of 2022 Oct 06.
def cgg_max_1340_uvt_deduction_and_max_4_dependents_72_uvt_each (
    row : pd.Series
)      -> float:
  a1 =   row ["renta liquida"] - 1340 * muvt
  a2  = ( row ["renta liquida"] * (1 - 0.325) -
         row ["dependents to claim (up to 4)"] * 72 * muvt )
  return max ( 0, a1, a2 )

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
