import pandas as pd
import numpy as np

import python.util as util
import python.vat.build.classes as classes
import python.vat.build.common as common
import python.vat.build.main as data



df0 = data.purchases[ data.purchases[ "coicop" ] . isnull() ]
util.dwmByGroup( "file-origin", df0 )

for c in data.people.filter(regex="income").columns:
  util.describeWithMissing( data.people[[c]] )


### How I determined which "total labor income" variable to use, and which to ignore.

df = data.people.filter(regex="labor").copy()
df = df[ (df.T != 0).any() ] # delete the all-zero rows

df = df.rename( columns = dict( zip(
  df.columns,
  ["formal", "contractor", "rural business", "all ? 1", "all ? 2"] ) ) )

df["formal - ?1"] = df["formal"] - df["all ? 1"]
df["formal - ?2"] = df["formal"] - df["all ? 2"]

dfc = df.drop( columns = ["contractor", "rural business"] )

util.describeWithMissing( dfc )


####

data.people["beca"].unique()
non_numbers = people["female"].str.contains( "[^0-9\.\,]", regex=True )

for c in data.people.columns:
  util.describeWithMissing( data.people[[c]] )


## older; to check the values present in the data against those described in the data documentation.

file_names = [
    "articulos"
  , "medios"
  , "rural capitulo c"
  , "urban capitulo c"
  , "rural_personal"
  , "rural_personal_fuera"
  , "rural_semanal"
  , "rural_semanal_fuera"
  , "urban_diario"
  , "urban_diario_fuera"
  , "urban_diario_personal"
  , "urban_personal_fuera"
  ]

df = enph.purchases

def check(file_name,col_name):
  dff = df[ df["file-origin"]==file_name ]
  vals = list( dff[col_name].unique() )
  for i in sorted( [str(v) for v in vals] ):
    print(i)

for fn in file_names:
  print("\n\n" + fn)
  check(fn,"freq")
