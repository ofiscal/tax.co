import pandas as pd
import python.build.output_io as oio
# import python.build.common as c


hs = pd.DataFrame( { "household" :     [10,11, 22,23]
                   , "income-decile" : [0,0,   1,1]
} )

ps = pd.DataFrame( { "household" : [10,10, 11,11,11, 22,22,22, 23,23]
                   , "value" :     [10,5,  10,5,1,   1,10,100, 1,10]
                   , "coicop" :    [1,2,   1,2,3,    1,2,3,    1,2]
} )

ps = ps.merge( hs, on = "household" )

ps  . groupby( ["income-decile","coicop"]
  ) . agg( {"value":"sum"}
  ) . sort_values( "value"
                 , ascending = False
  ) . reset_index(
  ) . groupby( ["income-decile"]
  ) . head( 2
  ) . sort_values( ["income-decile","value"]
                 , ascending = [True,False] )
