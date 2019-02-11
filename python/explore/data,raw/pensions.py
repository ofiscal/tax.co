import sys
import numpy as np
import pandas as pd
import re as regex


ppl = pd.read_csv(
  "data/enph-2017/recip-100/Caracteristicas_generales_personas.csv"
  , usecols = ["DIRECTORIO", "ORDEN", "FEX_C"
               ,"P6920", "P6920S1", "P6940", "P6990"]
  ) . rename( columns = { "DIRECTORIO" : "household"
                        , "ORDEN"      : "household-member"
                        , "FEX_C"      : "weight"
                        , "P6920"      : "pension, contributing, pre"
                        , "P6920S1"    : "pension, contribution amount"
                        , "P6940"      : "pension, contributors, pre"
                        , "P6990"      : "seguro de riesgos laborales, pre" } )

# This cannot be done until 'Object's are converted to numbers.
ppl["pension, contributing"] = ppl["pension, contributing, pre"] . apply(
  lambda x: 1 if x==1 else (0 if x==2 else np.nan) )
