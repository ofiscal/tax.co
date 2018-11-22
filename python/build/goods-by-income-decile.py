import pandas as pd
import python.build.output_io as oio
import python.util as util
import python.build.common as common


## ## ## ## ## Ingest data ## ## ## ## ##

# PITFALL: Always the detail vat strategy, because irrelevant.
hs = oio.readStage( common.subsample
                  , "households." + "detail_"
                  , usecols = ["household", "income-decile"]
)

ps = oio.readStage( common.subsample, 'purchases_1_5_no_origin'
                  , usecols = ["household", "value", "coicop"]  
)
ps = ps[ ~ ps["coicop"] . isnull() ] # purchases coded by cap c, not coicop: discard
ps["coicop"] = util.pad_column_as_int( 8, ps["coicop"] )
ps["coicop-2-digit"] = ps["coicop"] . apply( lambda s: s[0:2] )
ps["coicop-3-digit"] = ps["coicop"] . apply( lambda s: s[0:3] )

tax_proposed_2_digit = pd.read_csv( "python/build/vat_prop.2018_11_31/2-digit.csv"
                                    , usecols = ["coicop-2-digit","vat"] )
tax_proposed_2_digit = tax_proposed_2_digit[ tax_proposed_2_digit["vat"] > 0 ]
tax_proposed_2_digit["coicop-2-digit"] = (
  util.pad_column_as_int( 2, tax_proposed_2_digit["coicop-2-digit"] ) )

tax_proposed_3_digit = pd.read_csv( "python/build/vat_prop.2018_11_31/3-digit.csv"
                                    , usecols = ["coicop-3-digit","vat"] )
tax_proposed_3_digit = tax_proposed_3_digit[ tax_proposed_3_digit["vat"] > 0 ]
tax_proposed_3_digit["coicop-3-digit"] = (
  util.pad_column_as_int( 3, tax_proposed_3_digit["coicop-3-digit"] ) )

currently_untaxed = pd.read_csv( "data/vat/vat-by-coicop.csv"
                           , sep=";"
                           , usecols = ["coicop", "vat, max", "description"] )
currently_untaxed = currently_untaxed[ currently_untaxed["vat, max"] <= 0 ]
currently_untaxed["coicop"] = util.pad_column_as_int( 8, currently_untaxed["coicop"] )


## ## ## ## ## Isolate to the "vat-marginal" COICOP codes ## ## ## ## ##
# (that is, codes for which the current regime does not impose VAT while the proposal does)

ps = ps.merge( currently_untaxed, how = "right", on = "coicop" )
ps_2_digit = ps.merge( tax_proposed_2_digit, how = "right"
                     , on="coicop-2-digit" )
ps_3_digit = ps.merge( tax_proposed_3_digit, how = "right"
                     , on="coicop-3-digit" )
ps = ps_2_digit . combine_first( ps_3_digit
     )
ps = ps[["household", "coicop", "value", "description"]]


## ## ## ## ## Group ## ## ## ## ##

ps = ps.merge( hs, on = "household" )

grouped = ps . groupby( ["income-decile","coicop"]
  ) . agg( { "value":"sum"
           , "description": "first" }
  ) . sort_values( "value"
                 , ascending = False
  ) . reset_index(
  ) . groupby( ["income-decile"]
  ) . head( 20
  ) . sort_values( ["income-decile","value"]
                 , ascending = [True,False]
)

grouped.to_csv( "output/vat/tables/recip-" + str(common.subsample) + "/goods_by_income_decile.csv" )
