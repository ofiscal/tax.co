if True:
  import pandas                as pd
  #
  from   python.common.misc import muvt


### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Some algorithms to compute the cedula general gravable
### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def cgg_default ( row: pd.Series ) -> float:
  """
  The first stage of "renta gravable laboral" is someone's income,
  minus either 32.5% or 5040 UVTs, whichever is smaller.
  If someone cannot claim dependents,
  then their second stage renta gravable equals the first.
  If they can, and S1 is the value of the first stage,
  then the second stage is equal to S1 minus 10% or 32 UVT,
  whichever is smaller.
  """
  rlt = ( # "renta liquida trabajo", a term used in the tax code.
    # We ASSUME here that people are able to deduct the full 40%.
    # In reality what they are able to deduct depends on what they own --
    # owning a house helps, having a prepagada health plan helps, etc.
    # Note that the only people to whom this assumption matters
    # are the relatively well off, because nobody else pays income tax.
    row              ["renta liquida"]
    - min( 0.4 * row ["renta liquida"],
           5040 * muvt ) )
  stage2 = ( # TODO : Is there a name in the tax code for this?
    # Note that the calculations of rlt and stage2 are similar.
    # The assumption in the computation of rlt described above
    # implies that, unless one of the absolute thresholds
    # (5040 and/or 2880 UVT) applies, the taxpayer only pays tax on
    # 45% of their income, because- 45% = (1 - 0.4) * (1 - 0.25)
    rlt
    - min ( 0.25 * rlt,
            2880 * muvt ) )
  stage3 = ( stage2 if not row["claims dependent (labor income tax)"]
             else  stage2 - min( 0.1 * stage2,
                                 32 * muvt ) )
  return stage3

def cgg_single_2052_UVT_income_tax_deduction ( row: pd.Series ) -> float:
  stage1 = max ( row ["renta liquida"] - 2052 * muvt,
                 0 )
  return ( stage1
           if not row["claims dependent (labor income tax)"]
           else  stage1 - min( 0.1 * stage1,
                               32 * muvt ) )
