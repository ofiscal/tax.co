import python.vat.build.main as data  

import python.util as util
import python.vat.build.classes as classes
import python.vat.build.common as common

import pandas as pd
import numpy as np
import re as regex

import python.vat.build.buildings.files as bldg
import python.vat.build.people.files as ppl
import python.vat.build.purchases.nice_purchases as nice_purchases
import python.vat.build.purchases.medios as medios
import python.vat.build.purchases.articulos as articulos
import python.vat.build.purchases.capitulo_c as capitulo_c



df = pd.DataFrame( [[1,2],[3,np.nan]], columns = ["a","b"] )
df2 = df.drop( df[ df["a"]==1 ].index )
df2
df3 = classes.Correction.Drop_Row_If_Column_Equals( "a", 1 ).correct( df )
df3

df = pd.read_csv( "data/enph-2017/recip-100/"
                  + "Gastos_diarios_Urbano_-_Capitulo_C.csv" )
df = pd.read_csv( "data/enph-2017/recip-100/"
                  + "Gastos_semanales_Rural_-_Capitulo_C.csv" )
df["NC2_CC_P3_S2"].unique()

dfd = classes.Correction.Drop_Row_If_Column_Equals(
  "NC2_CC_P3_S2", 2 ).correct( df )  
dfd["NC2_CC_P3_S2"].unique()

x = common.collect_files(
    capitulo_c.files
  )

x[ x["duplicated"]==2 ]["file-origin"].unique()
purchases[ purchases["duplicated"]==2 ]["file-origin"].unique()
data.purchases[ data.purchases["duplicated"]==2 ]["file-origin"].unique()

# Even when purhcase=1, in some files there are a substantial number
# of observations where where-got is missing.
util.dwmByGroup( "file-origin",
                 data.purchases[ data.purchases["is-purchase"]==1 ]
                 [["file-origin","freq"]] )

for c in data.people.filter(regex="income").columns:
  util.describeWithMissing( data.people[[c]] )


data.purchases[
  (~ data.purchases["coicop"].isnull())
  | (~ data.purchases["25-broad-categs"].isnull()) ].count()


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
