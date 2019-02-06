import sys
import pandas                    as pd

import python.build.ss_functions as ss
import python.build.output_io    as oio
import python.util               as util
import python.build.common       as c


people = oio.readStage( c.subsample
                      , "people_3_purchases." + c.vat_strategy_suffix )

people["4 por mil"] = 0.004 * (people["income, cash"] - 11.6e6)

for (goal,function) in [
      ("tax, pension"               , ss.mk_pension)
    , ("tax, pension, employer"     , ss.mk_pension_employer)
    , ("tax, salud"                 , ss.mk_salud)
    , ("tax, salud, employer"       , ss.mk_salud_employer)
    , ("tax, solidaridad"           , ss.mk_solidaridad)
    , ("tax, parafiscales"          , ss.mk_parafiscales_employer)
    , ("tax, cajas de compensacion" , ss.mk_cajas_de_compensacion_employer)
    , ("cesantias + primas"         , ss.mk_cesantias_employer) ]:
  people[goal] = people.apply(
      lambda row: function( row["independiente"], row["income, labor, cash"] )
    , axis = "columns" )

oio.saveStage( c.subsample
             , people
             , 'people_4_ss.' + c.vat_strategy_suffix
)
