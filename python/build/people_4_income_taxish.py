# Compute how much a person paid for various income taxes,
# and for things resembling income tax, e.g. social security contributions.

if True:
  import sys
  import pandas                    as pd
  #
  import python.build.ss_functions as ss
  import python.build.output_io    as oio
  import python.common.util        as util
  import python.common.misc        as m
  import python.common.common      as com
  #
  if com.regime_year == 2016:
        import python.regime.r2016 as regime
  else: import python.regime.r2018 as regime


ppl = oio.readStage( com.subsample
                   , "people_3_purchases." + com.strategy_suffix )

# This tax is also known as the "4 por mil" --
# the 0.4% tax levided on transactions involving someone's bank account.
ppl["tax, gmf"] = (0.004 * ( ppl["income, cash"] - m.gmf_threshold)
                  ).apply( lambda x: max(0,x) )

ppl["tax, ganancia ocasional"] = (
  ppl["income, ganancia ocasional, 10%-taxable"] * 0.1 +
  ppl["income, ganancia ocasional, 20%-taxable"] * 0.2 )

for (goal,function) in [
      ("tax, ss, pension"               , ss.mk_pension)
    , ("tax, ss, pension, employer"     , ss.mk_pension_employer)
    , ("tax, ss, salud"                 , ss.mk_salud)
    , ("tax, ss, salud, employer"       , ss.mk_salud_employer)
    , ("tax, ss, solidaridad"           , ss.mk_solidaridad)
    , ("tax, ss, parafiscales"          , ss.mk_parafiscales_employer)
    , ("tax, ss, cajas de compensacion" , ss.mk_cajas_de_compensacion_employer)
    , ("cesantias + primas"             , ss.mk_cesantias_y_primas_employer) ]:
  ppl[goal] = ppl.apply(
      lambda row: function( row["independiente"], row["income, labor, cash"] )
    , axis = "columns" )

ppl["tax, ss, total employee contribs"] = (
  ppl["tax, ss, pension"] +
  ppl["tax, ss, salud"] +
  ppl["tax, ss, solidaridad"] )

# Determine dependents, for income tax, assuming rationality -- that is,
# the highest earner should claim the first available dependent,
# the next-highest earner should claim the next available dependent, etc.
if True:
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

ppl = regime.income_taxes( ppl )

oio.saveStage( com.subsample
             , ppl
             , 'people_4_income_taxish.' + com.strategy_year_suffix
)
