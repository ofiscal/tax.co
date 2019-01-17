import sys
import pandas as pd
import python.build.output_io as oio
import python.build.ss_contribs as ss
import python.build.common as c


people = oio.readStage( c.subsample
                      , "people_3_purchases." + c.vat_strategy_suffix )

ss_contrib_schedules = {
    "pension" : {
      "independiente" : [ (0  , 0.0)
                     , (1e6, 0.1)
                     , (5e6, 0.2) ]
      , "asalariado" : [ (0  , 0.1)
                     , (1e6, 0.2)
                     , (5e6, 0.3) ]
    } , "salud" :  {
      "independiente" : [ (0  , 0.01)
                     , (1e6, 0.01)
                     , (5e6, 0.02) ]
      , "asalariado" : [ (0  , 0.01)
                     , (1e6, 0.02)
                     , (5e6, 0.03) ]
    } , "solidaridad" :  {
      "independiente" : [ (0  , 0.001)
                     , (1e6, 0.001)
                     , (5e6, 0.002) ]
      , "asalariado" : [ (0  , 0.001)
                     , (1e6, 0.002)
                     , (5e6, 0.003) ]
    }
  }

ss_df = ss.ss_contribs( ss_contrib_schedules
                      , people["independiente"]
                      , people["income, labor"]
)

people = people.merge( ss_df, right_index=True, left_index=True )

oio.saveStage( c.subsample
             , people
             , 'people_4_ss.' + c.vat_strategy_suffix
)
