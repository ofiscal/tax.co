import sys
import numpy as np
import pandas as pd
import re as regex
import python.common.misc as c
import python.common.cl_fake as cl
import python.util as util


colDict = { "DIRECTORIO" : "household"
          , "ORDEN"      : "household-member"
          , "FEX_C"      : "weight"
          , "P6920"      : "pension, contributing, pre"
          , "P6920S1"    : "pension, contribution amount"
          , "P6940"      : "pension, contributors, pre"
          , "P7500S2A1"  : "pension, receipts"
            # new name, old income variable
          , "P6990"      : "seguro de riesgos laborales, pre" }

ppl = pd.read_csv(
  "data/enph-2017/recip-" + str(cl.subsample)
  + "/Caracteristicas_generales_personas.csv"
  , usecols = list( colDict.keys() )
  ) . rename( columns = colDict )

for corr in c.corrections:
  ppl = corr.correct( ppl )

ppl = c.to_numbers(ppl)

# This cannot be done until 'Object's are converted to numbers.
ppl["pension, contributing"] = ppl["pension, contributing, pre"] . apply(
  lambda x: 1 if x==1 else ( 0 if x==2 else np.nan ) )

ppl["pension, receiving"] = (   ( ppl["pension, contributing, pre"] == 3 )
                              | ( ppl["pension, receipts"] > 0 )
                            ) . astype('int')

ppl["pension, contributor(s) = split"] = (
  ppl["pension, contributors, pre"]
  ) . apply( lambda x: 1 if x == 1 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) )

ppl["pension, contributor(s) = self"] = (
  ppl["pension, contributors, pre"]
  ) . apply( lambda x: 1 if x == 2 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) )

ppl["pension, contributor(s) = employer"] = (
  ppl["pension, contributors, pre"]
  ) . apply( lambda x: 1 if x == 3 else
             ( 0 if (x > 0) & (x < 4) else np.nan ) )

ppl["seguro de riesgos laborales"] = (
  ppl["seguro de riesgos laborales, pre"]
  . apply( lambda x: 1 if x==1 else (0 if x==2 else np.nan) ) )
# ppl[["seguro de riesgos laborales", "seguro de riesgos laborales, pre"]]

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
