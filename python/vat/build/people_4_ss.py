import sys
import pandas as pd
import python.vat.build.output_io as oio
import python.vat.build.ss_contribs as ss
import python.vat.build.common as common


people = oio.readStage( common.subsample
                      , "people_3_purchases." + common.vat_strategy_suffix )

ss_contrib_schedules = {
    "pension" : {
      "contractor" : [ (0  , 0.0)
                     , (1e6, 0.1)
                     , (5e6, 0.2) ]
      , "employee" : [ (0  , 0.1)
                     , (1e6, 0.2)
                     , (5e6, 0.3) ]
    } , "salud" :  {
      "contractor" : [ (0  , 0.01)
                     , (1e6, 0.01)
                     , (5e6, 0.02) ]
      , "employee" : [ (0  , 0.01)
                     , (1e6, 0.02)
                     , (5e6, 0.03) ]
    } , "solidaridad" :  {
      "contractor" : [ (0  , 0.001)
                     , (1e6, 0.001)
                     , (5e6, 0.002) ]
      , "employee" : [ (0  , 0.001)
                     , (1e6, 0.002)
                     , (5e6, 0.003) ]
    }
  }

ss_df = ss.ss_contribs( ss_contrib_schedules
                      , people["contractor"]
                      , people["income, labor"]
)

people = people.merge( ss_df, right_index=True, left_index=True )

oio.saveStage( common.subsample
             , people
             , 'people_4_ss.' + common.vat_strategy_suffix
)
