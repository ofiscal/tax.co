# Compute how much a person paid for various income taxes,
# and for things resembling income tax, e.g. social security contributions.

if True:
  import sys
  import pandas                    as pd
  #
  import python.build.ss_functions as ss
  import python.build.output_io    as oio
  import python.common.util        as util
  import python.common.common      as com
  #
  import python.build.people_3_income_taxish_functions as f4
  if   com.regime_year == 2016:
      import python.regime.r2016 as regime
  elif com.regime_year == 2018:
      import python.regime.r2018 as regime
  else:
      import python.regime.r2019 as regime


ppl = oio.readStage( com.subsample
                   , "people_2_buildings" )

ppl = ss.mk_ss_contribs(ppl)

ppl = f4.insert_has_dependent_column(ppl)

ppl = regime.income_taxes( ppl )

oio.saveStage( com.subsample
             , ppl
             , 'people_3_income_taxish.' + com.strategy_year_suffix
)

