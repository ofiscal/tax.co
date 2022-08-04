if True: # imports
  from os import path
  import pandas                as pd
  #
  import python.common.common  as com
  import python.common.misc    as misc
  from   python.common.misc import muvt
  import python.common.terms   as terms
  import python.regime.strategy_dependent as strat_dep
  if True: # CSV-dynamic imports
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
  if com.strategy == terms.single_2052_UVT_income_tax_deduction:
    return strat_dep . cgg_single_2052_UVT_income_tax_deduction ( row )
  if com.strategy == terms.detail:
    return strat_dep . cgg_default                              ( row )
