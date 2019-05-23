##### descriptive stats on pensions #####
#
# These variables are in 'caracteristicas generales'.
# ** DONE contributing to pension = P6920 == 1
# If that's 2, this is 0.
# If that's 3, this is NaN.
# ** pensioned = P6920 == 3
# If that's 1 or 2, this is 0.
# ** pension contribution amount = P6920S1
# ** pension contribution participants
# splitting pension contribs with employer = P6940 == 1
# worker paying the whole contrib = P6940 == 2
# employer paying the whole contrib = P6940 == 3
# ** P6990 = Aseguradora de Riesgos Laborales
# 1 -> 1 = has
# 2 -> 0 = does not have
# 3 -> NaN = does not know

import sys
import numpy as np
import pandas as pd
import python.common.misc as c
import python.common.cl_fake as cl
import python.common.util as util


colDict = { "DIRECTORIO" : "household"
          , "ORDEN"      : "household-member"
          , "FEX_C"      : "weight"
          , "P6920"      : "pension, contributing, pre"
          , "P6920S1"    : "pension, contribution amount"
          , "P6940"      : "pension, contributors, pre"
          , "P6990"      : "seguro de riesgos laborales, pre"
          , "P7500S2A1"  : "pension, receipts"
            # new name, old income variable
}

ppl = pd.read_csv(
  "data/enph-2017/recip-" + str(cl.subsample)
  + "/Caracteristicas_generales_personas.csv"
  , usecols = list( colDict.keys() )
  ) . rename( columns = colDict )

for corr in c.corrections:
  ppl = corr.correct( ppl )

ppl = c.all_columns_to_numbers(ppl)

ppl["pension, contributing (if not pensioned)"] = (
  ppl["pension, contributing, pre"]
  . apply( lambda x: 1 if x==1 else ( 0 if x==2 else np.nan ) ) )

ppl["pension, receiving"] = (   ( ppl["pension, contributing, pre"] == 3 )
                              | ( ppl["pension, receipts"] > 0 )
                            ) . astype('int')

ppl["pension, contributor(s) (if not pensioned) = split"] = (
  ppl["pension, contributors, pre"]
  . apply( lambda x: 1 if x == 1 else
           ( 0 if (x > 0) & (x < 4) else np.nan ) ) )

ppl["pension, contributor(s) (if not pensioned) = self"] = (
  ppl["pension, contributors, pre"]
  . apply( lambda x: 1 if x == 2 else
           ( 0 if (x > 0) & (x < 4) else np.nan ) ) )

ppl["pension, contributor(s) (if not pensioned) = employer"] = (
  ppl["pension, contributors, pre"]
  . apply( lambda x: 1 if x == 3 else
           ( 0 if (x > 0) & (x < 4) else np.nan ) ) )

ppl["seguro de riesgos laborales"] = (
  ppl["seguro de riesgos laborales, pre"]
  . apply( lambda x: 1 if x==1 else (0 if x==2 else np.nan) ) )

ppl["x"] = (
    ppl["seguro de riesgos laborales, pre"] .astype('str')
  + ppl["seguro de riesgos laborales"]      .astype('str')
  )
ppl["x"].unique()

ppl["one"] = 1
stats = []
for col in ppl.columns:
  df = util.tabulate_stats_by_group( ppl, "one", col, "weight" )
  df["column"] = col
  stats.append(df)

stats = pd.concat( stats
      ). set_index( "column"
      ) . drop( index = ["household", "household-member", "weight"
                        , "pension, contributing, pre"
                        , "pension, contributors, pre"
                        , "seguro de riesgos laborales, pre" ] )

stats.to_csv( "output/pensions.csv" )
