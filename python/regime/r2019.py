if True: # imports
  from os import path
  import pandas                                 as pd
  #
  import python.common.common                   as com
  import python.common.misc                     as misc
  import python.common.terms                    as terms
  import python.regime.cedula_general_gravable  as cgg
  if True: # CSV-dynamic imports
    rates = path.join( "users", com.user, "config/marginal_rates" )
    for lib in ["dividend",
                "ocasional_low",
                "ocasional_high",
                "most",]:
      # TODO : The Makefile does not know about these imports.
      # PITFALL: Mypy cannot not understand these imports.
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
  """PITFALL: Destructive.
  TODO: It would be less confusing,
  rather than maintaining temp_columns and new_columns as separate frames,
  to just create everything in ppl and then delete the temp columns.
  Maybe there's a speed argument for separating them; I don't remember.
  """
  temp_columns = pd.DataFrame()
  temp_columns["dependents to claim (up to 4)"] = \
    ppl [      "dependents to claim (up to 4)"]
  temp_columns["claims dependent (labor income tax)"] = (
    ppl [      "claims dependent (labor income tax)"] )
  temp_columns["zero"] = 0
  temp_columns["renta liquida"] = (
    # This is taxable labor income before exemptions.
    ( ( ppl["income, labor"]
      - ppl["tax, ss, total employee contribs"] )
    ) )
  temp_columns["cedula general gravable"] = (
    temp_columns .
    apply ( cgg . cedula_general_gravable, axis = 1 ) )

  new_columns = (
    # Some of the new_columns data depends on com.strategy.
    # This determines that stuff.
    { terms.detail
      : new_columns__detail,
      terms.reduce_income_tax_deduction_to_1210_uvts
      : new_columns__detail,
      terms.max_1340_uvt_deduction_and_max_4_dependents_72_uvt_each
      : new_columns__detail,
      terms.single_cedula_with_single_1210_uvt_threshold
      : new_columns__single_cedula_with_single_1210_uvt_threshold }
    [ com.strategy ] # Look up a function from the dictionary.
    ( ppl = ppl, # Apply arguments to the function.
      temp_columns = temp_columns ) )
  # These elements of new_columns are independent of com.strategy.
  new_columns ["tax, income, gmf"] = (
    # a.k.a. the "4 por mil" -- a 0.4% tax
    # levided on transactions involving someone's bank account.
    ( 0.004 * ( ppl["income, cash"] - misc.gmf_threshold) )
    . apply( lambda x: max(0,x) ) )
  new_columns["tax, income"] = (
      new_columns [ income_tax_components ] .
      sum ( axis = "columns" ) )
  return pd.concat( [ppl, new_columns], axis = 1 )

def new_columns__detail (
    ppl : pd.DataFrame,
    temp_columns : pd.DataFrame
) -> pd.DataFrame:
  ret = pd.DataFrame()
  ret["tax, income, most"] = (
    ( temp_columns[["cedula general gravable","zero"]]
      . max ( axis = "columns" ) # Takes the row-wise maximum.
      + ppl["income, rental + interest"]
      + ppl["income, non-labor (tax def)"]
      + ppl["income, pension"] )
    . apply( rates_most . f ) )
  ret["tax, income, dividend"] = (
    ppl["income, dividend"].apply(
        rates_dividend . f ) )
  ret["tax, income, ganancia ocasional"] = (
    ( ppl["income, ganancia ocasional, 10%-taxable"]
      . apply ( rates_ocasional_low . f ) ) +
    ( ppl["income, ganancia ocasional, 20%-taxable"]
      . apply ( rates_ocasional_high . f ) ) )
  return ret

def new_columns__single_cedula_with_single_1210_uvt_threshold (
    ppl : pd.DataFrame,
    temp_columns : pd.DataFrame
) -> pd.DataFrame:
  ret = pd.DataFrame()
  ret["tax, income, most"] = (
    ( temp_columns[["cedula general gravable","zero"]]
      . max ( axis = "columns" ) # Takes the row-wise maximum.
      + ppl["income, rental + interest"]
      + ppl["income, non-labor (tax def)"]
      + ppl["income, pension"]
      + ppl["income, dividend"]
      + ppl["income, ganancia ocasional, 10%-taxable"]
      + ppl["income, ganancia ocasional, 20%-taxable"]
     )
    . apply( rates_most . f ) )
  ret["tax, income, dividend"] = 0
  ret["tax, income, ganancia ocasional"] = 0
  return ret
