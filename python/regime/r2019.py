if True: # imports
  from os import path
  import pandas as pd
  import python.common.common as com
  import python.common.misc as misc
  from   python.common.misc import muvt
  if True: # csv-dynamic imports
    rates = path.join( "users", com.user, "config/marginal_rates" )
    for lib in ["dividend",
                "ocasional_low",
                "ocasional_high",
                "most",]:
      # PITFALL: Mypy does not understand this.
      # The exec statement constructs an alias, "rates_x" (for some x),
      # for each library it imports -- the full list of those libraries
      # being the arguments to the for loop above.
      # If mypy says something like `Name "rates_most" is not defined`,
      # that's why.
      exec( "import "
            + ( path.join( rates, lib )
              . replace ( "/", "." ) )
            + " as rates_" + lib )


income_tax_components = [ "tax, income, most",
                          "tax, income, dividend",
                          "tax, income, ganancia ocasional",
                          "tax, income, gmf",
                        ]

income_tax_columns = [ "tax, income" ] + income_tax_components

def income_taxes( ppl : pd.DataFrame ) -> pd.DataFrame:
  """PITFALL: Destructive."""
  new_columns = pd.DataFrame()
  temp_columns = pd.DataFrame()
  temp_columns["claims dependent (labor income tax)"] = (
    ppl["claims dependent (labor income tax)"] )
  temp_columns["zero"] = 0
  temp_columns["renta liquida"] = (
    # This is taxable labor income before exemptions.
    ( ( ppl["income, labor"]
      - ppl["tax, ss, total employee contribs"] )
    ) )

  temp_columns["cedula general gravable"] = (
    temp_columns .
    apply ( cedula_general_gravable, axis = 1 ) )

  new_columns["tax, income, most"] = (
    ( temp_columns[["cedula general gravable","zero"]]
      . max ( axis = "columns" ) # Takes the row-wise maximum.
      + ppl["income, rental + interest"]
      + ppl["income, non-labor (tax def)"]
      + ppl["income, pension"] )
    . apply( rates_most . f ) )

  new_columns["tax, income, dividend"] = (
    ppl["income, dividend"].apply(
        rates_dividend . f ) )

  new_columns["tax, income, ganancia ocasional"] = (
    ( ppl["income, ganancia ocasional, 10%-taxable"]
      . apply ( rates_ocasional_low . f ) ) +
    ( ppl["income, ganancia ocasional, 20%-taxable"]
      . apply ( rates_ocasional_high . f ) ) )

  # a.k.a. the "4 por mil" -- a 0.4% tax
  # levided on transactions involving someone's bank account.
  new_columns["tax, income, gmf"] = (
      0.004 * ( ppl["income, cash"] - misc.gmf_threshold)
      ).apply( lambda x: max(0,x) )

  new_columns["tax, income"] = (
      new_columns [ income_tax_components ] .
      sum ( axis = "columns" ) )

  return pd.concat( [ppl, new_columns], axis = 1 )

def cedula_general_gravable ( row: pd.Series ) -> float:
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
