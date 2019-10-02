import pandas as pd
import numpy as np

import python.build.output_io as oio


subsample = 10
purchases = oio.readStage( subsample, "purchases_2_vat" )

purchases["purchases"] = 1

# When I check purchases[ purchases["coicop"] == x ] for these x,
# the results are consistent with the coicop-vat bridge.
# 11110103, 11110104, 11110105
# 1119807, 1119808, 1119809
# 1180103, 1180201, 1180301


## vat per coicop
p_sum = purchases.groupby( 'coicop' )[ "value" ] . agg( 'sum' )
p_first = purchases.groupby( 'coicop' )[ "vat, min" ] . agg( 'mean' )
p = pd.concat( [p_sum, p_first]
              , axis = 1 )

oio.saveStage( subsample, p, "vat-and-spending-per-coicop"
               , index = True
)


## vat per rate
q_sum = purchases.groupby( 'vat, min' )[ "value" ] . agg( 'sum' )
q_first = purchases.groupby( 'vat, min' )[ "vat, min" ] . agg( 'mean' )
q = pd.concat( [q_sum, q_first]
              , axis = 1 )

oio.saveStage( subsample, q, "vat-and-spending-per-vat-rate"
               , index = True
)
