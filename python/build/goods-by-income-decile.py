import pandas as pd
import python.build.output_io as oio
import python.util as util
#import python.build.common as common


class common:
  subsample=100


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
ps["coicop-2-digit"] = purchases["coicop"] . apply( lambda s: s[0:2] )
ps["coicop-3-digit"] = purchases["coicop"] . apply( lambda s: s[0:3] )

proposed_rates_2_digit = pd.read_csv( "python/build/vat_prop.2018_11_31/2-digit.csv"
                                    , usecols = ["coicop-2-digit","vat"] )
proposed_rates_2_digit = proposed_rates_2_digit[ proposed_rates_2_digit["vat"] > 0 ]
proposed_rates_2_digit["coicop-2-digit"] = (
  util.pad_column_as_int( 2, proposed_rates_2_digit["coicop-2-digit"] ) )

proposed_rates_3_digit = pd.read_csv( "python/build/vat_prop.2018_11_31/3-digit.csv"
                                    , usecols = ["coicop-3-digit","vat"] )
proposed_rates_3_digit = proposed_rates_3_digit[ proposed_rates_3_digit["vat"] > 0 ]
proposed_rates_3_digit["coicop-3-digit"] = (
  util.pad_column_as_int( 3, proposed_rates_3_digit["coicop-3-digit"] ) )

current_rates = pd.read_csv( "data/vat/vat-by-coicop.csv"
                           , sep=";"
                           , usecols = ["description", "coicop", "vat, max"] )
current_rates = current_rates[ current_rates["vat, max"] <= 0 ]
current_rates["coicop"] = util.pad_column_as_int( 8, current_rates["coicop"] )


## ## ## ## ## Find the COICOP codes of interest ## ## ## ## ##




## ## ## ## ## Group ## ## ## ## ##

ps = ps.merge( hs, on = "household" )

grouped = ps  . groupby( ["income-decile","coicop"]
  ) . agg( {"value":"sum"}
  ) . sort_values( "value"
                 , ascending = False
  ) . reset_index(
  ) . groupby( ["income-decile"]
  ) . head( 20
  ) . sort_values( ["income-decile","value"]
                 , ascending = [True,False]
)

out = grouped.merge( current_rates, how="left", on="coicop" )

out.to_csv( "output/vat/tables/recip-" + str(common.subsample) + "/goods_by_income_decile.csv" )
