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
      exec( "import "
            + ( path.join( rates, lib )
              . replace ( "/", "." ) )
            + " as rates_" + lib )


income_tax_columns = [ "tax, income"
                     , "tax, income, most"
                     , "tax, income, dividend"
                     , "tax, income, ganancia ocasional"
                     , "tax, income, gmf"
                     ]

gravable_pre = "cedula general gravable, sums before exemptions"

def income_taxes( ppl : pd.DataFrame ) -> pd.DataFrame:
  """PITFALL: Destructive."""
  new_columns = pd.DataFrame()
  temp_columns = pd.DataFrame()
  temp_columns["claims dependent (labor income tax)"] = ppl["claims dependent (labor income tax)"]
  temp_columns[gravable_pre] = (
    ( ( ppl["income, labor"]
      - ppl["tax, ss, total employee contribs"] )
    + ppl["income, rental + interest"]
    + ppl["income, non-labor (tax def)"]
    ) )

  temp_columns["cedula general gravable"] = (
    temp_columns .
    apply ( taxable, axis = 1 ) )

  new_columns["tax, income, most"] = (
    ( temp_columns["cedula general gravable"] +
      ppl["income, pension"] )
    . apply( rates_most . f ) )

  new_columns["tax, income, dividend"] = (
    ppl["income, dividend"].apply(
        rates_dividend.f ) )

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

  # TODO: This is dangerous: It duplicates some information from
  # income_tax_columns, so they can get out of sync.
  new_columns["tax, income"] = (
      new_columns [[ "tax, income, most"
                   , "tax, income, dividend"
                   , "tax, income, ganancia ocasional"
                   , "tax, income, gmf" ]] .
      sum( axis = "columns" ) )

  return pd.concat( [ppl, new_columns], axis = 1 )

def taxable( row: pd.Series ) -> float:
  """
  The first stage of "renta gravable laboral" is someone's income,
  minus either 32.5% or 5040 UVTs, whichever is smaller.
  If someone cannot claim dependents, then their second stage renta gravable
  is the same as the first.
  If they can, and S1 is the value of the first stage,
  then the second stage is equal to S1 minus 10% or 32 UVT,
  whichever is smaller.
  """
  s1 = (
    row               [gravable_pre]
    - min( 0.325 * row[gravable_pre],
           5040 * muvt ) )
  s2 = ( s1 if not row["claims dependent (labor income tax)"]
         else  s1 - min( 0.1 * s1,
                         32 * muvt ) )
  return s2
