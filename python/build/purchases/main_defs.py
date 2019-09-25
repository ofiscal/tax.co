def drop_if_coicop_or_value_invalid( df ):
  """ Include only rows with a coicop-like variable and a value."""
  # Why: For every file but "articulos", observations with no coicop have
  # no value, quantity, is-purchase or frequency. And only 63 / 211,000
  # observations in "articulos" have a missing COICOP. A way to see that
    # (which works if the file-origin variable is reenabled):
    # df0 = data.purchases[ data.purchases[ "coicop" ] . isnull() ]
    # util.dwmByGroup( "file-origin", df0 )
  return df[ ( (  ~ df[ "coicop"          ] . isnull())
               | (~ df[ "25-broad-categs" ] . isnull()) )
             & (  ~ df[ "value"           ] . isnull()) ]

absurdly_big_expenditure_threshold = 1e9

def drop_absurdly_big_expenditures( df ):
  return df[ ~(df["value"] > absurdly_big_expenditure_threshold) ]

