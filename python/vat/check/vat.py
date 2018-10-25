# exec( open( "python/vat/check/vat.py" ) . read() )

exec( open( "python/vat/check/read.py" ) . read() )


coicop_2_digit = pd.read_csv( "python/vat/build/vat_approx/2-digit.csv"
                            , usecols = ["coicop-2-digit","vat"] )
coicop_3_digit = pd.read_csv( "python/vat/build/vat_approx/3-digit.csv"
                            , usecols = ["coicop-3-digit","vat"] )

coicop_2_digit["vat-frac"] = coicop_2_digit["vat"] . apply( lambda x : x / (1+x) )
coicop_3_digit["vat-frac"] = coicop_3_digit["vat"] . apply( lambda x : x / (1+x) )

coicop_2_digit['coicop-2-digit'] = coicop_2_digit['coicop-2-digit'] . apply( lambda x: '{0:0>2}'.format(x) )
coicop_3_digit['coicop-3-digit'] = coicop_3_digit['coicop-3-digit'] . apply( lambda x: '{0:0>3}'.format(x) )

purchases["coicop"]      = purchases     ["coicop"] . apply( lambda x: '{0:0>8}'.format(x) )
  # PITFALL: The previous line turns NaN into a string.
  # And I have to leave them that way until I've taking substrings, next.
purchases["coicop-2-digit"] = purchases["coicop"] . apply( lambda l: l[0:2] )
purchases["coicop-3-digit"] = purchases["coicop"] . apply( lambda l: l[0:3] )
  # Now I can convert missing values back to NaN.
purchases.loc[ purchases["coicop"] . str.contains( "[^0-9]" )
             , "coicop-2-digit"
             ] = np.nan
purchases.loc[ purchases["coicop"] . str.contains( "[^0-9]" )
             , "coicop-3-digit"
             ] = np.nan
purchases.loc[ purchases["coicop"] . str.contains( "[^0-9]" )
             , "coicop"
             ] = np.nan

purchases_2 = purchases.merge( coicop_2_digit, how = "left", on = "coicop-2-digit" )
purchases_3 = purchases.merge( coicop_3_digit, how = "left", on = "coicop-3-digit" )

purchases = purchases_2.combine_first( purchases_3 ) # Either order works here.
  # (In theory and after testing.)
purchases["one"] = 1

x = util.tabulate_stats_by_group( purchases, "one", "vat-frac", "weight" )
