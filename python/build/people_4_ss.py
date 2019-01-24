import sys
import pandas as pd
import python.build.ss_schedules as ss
import python.build.output_io as oio
import python.build.common as c


people = oio.readStage( c.subsample
                      , "people_3_purchases." + c.vat_strategy_suffix )

people["4 por mil"] = 0.004 * (people["income, cash"] - 11.6e6)

#def mk_pension ( independiente, income ):
#  if independiente:

# people = people.merge( << ss stuff >> )

oio.saveStage( c.subsample
             , people
             , 'people_4_ss.' + c.vat_strategy_suffix
)
