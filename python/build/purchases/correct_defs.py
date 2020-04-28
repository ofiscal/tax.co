def drop_if_coicop_or_value_invalid( df ):
  """Include only rows with a coicop-like variable and a value.
Purchases with no assigned peso value are useless to us.
Maybe we could use purchases with a value but no code
indicating the kind of purchase, but so far we do not.
That latter kind of observation ir rare --
for every file but "articulos", observations with no coicop have
no value, quantity, is-purchase or frequency. And only 63 / 211,000
observations in "articulos" have a missing COICOP. A way to see that
(which works if the file-origin variable is reenabled):
df0 = data.purchases[ data.purchases[ "coicop" ] . isnull() ]
util.dwmByGroup( "file-origin", df0 )"""
  return df[ ( (  ~ df[ "coicop"          ] . isnull())
               | (~ df[ "25-broad-categs" ] . isnull()) )
             & (  ~ df[ "value"           ] . isnull()) ]

absurdly_big_expenditure_threshold = 1e9 # MAGIC
  # It seems reasonable to us to discard purchases
  # bigger than this as probably errors. In future, after inflation,
  # this number could well change.

def drop_absurdly_big_expenditures( df ):
  return df[ ~(df["value"] > absurdly_big_expenditure_threshold) ]
