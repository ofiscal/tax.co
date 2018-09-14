# To check the values present in the data against those described in the data documentation.

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
