import pandas as pd
import python.build.output_io as oio
# import python.build.common as common


class common:
  subsample = 100
  vat_strategy_suffix = "detail_"

hs = oio.readStage( common.subsample, "households." + common.vat_strategy_suffix
                  , usecols = ["household", "income-decile"]
)

ps = oio.readStage( common.subsample, 'purchases_1_5_no_origin'
                  , usecols = ["household", "value", "coicop"]  
)

ps = ps.merge( hs, on = "household" )

ps  . groupby( ["income-decile","coicop"]
  ) . agg( {"value":"sum"}
  ) . sort_values( "value"
                 , ascending = False
  ) . reset_index(
  ) . groupby( ["income-decile"]
  ) . head( 20
  ) . sort_values( ["income-decile","value"]
                 , ascending = [True,False] )
