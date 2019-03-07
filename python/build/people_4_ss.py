import sys
import pandas                    as pd

import python.build.ss_functions as ss
import python.build.output_io    as oio
import python.util               as util
import python.common.misc as c
import python.common.cl_args as cl


ppl = oio.readStage( cl.subsample
                      , "people_3_purchases." + cl.vat_strategy_suffix )

ppl["4 por mil"] = 0.004 * (ppl["income, cash"] - 11.6e6)

for (goal,function) in [
      ("tax, pension"               , ss.mk_pension)
    , ("tax, pension, employer"     , ss.mk_pension_employer)
    , ("tax, salud"                 , ss.mk_salud)
    , ("tax, salud, employer"       , ss.mk_salud_employer)
    , ("tax, solidaridad"           , ss.mk_solidaridad)
    , ("tax, parafiscales"          , ss.mk_parafiscales_employer)
    , ("tax, cajas de compensacion" , ss.mk_cajas_de_compensacion_employer)
    , ("cesantias + primas"         , ss.mk_cesantias_employer) ]:
  ppl[goal] = ppl.apply(
      lambda row: function( row["independiente"], row["income, labor, cash"] )
    , axis = "columns" )

if True: # determine dependents, for income tax
  hh = ( ppl[["household","dependent"]]
         . groupby( "household" )
         . agg( 'sum' )
         . rename( columns = {"dependent":"dependents"} )
         . reset_index() )
  ppl = ( ppl.merge( hh, how='inner', on='household' )
          . drop( columns = "dependent" ) )
  ppl["has dependent"] = (
    ppl["member-by-income"] <= ppl["dependents"] )
  del(hh)

oio.saveStage( cl.subsample
             , ppl
             , 'people_4_ss.' + cl.vat_strategy_suffix
)
