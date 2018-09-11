# To check the values present in the data against those described in the data documentation.

filenames = [
    "urban_personal_fuera"
  , "urban_diario_fuera"
  , "urban_diario_personal"
  , "urban_diario"
  , "rural_personal_fuera"
  , "rural_personal"
  , "rural_semanal_fuera"
  , "rural_semanal"
  , "articulos"
  , "medios"
  , "urban capitulo c"
  , "rural capitulo c"
  ]

df = enph.purchases

def check(filename):
  dff = df[ df["file-origin"]==filename ]
  freqs = list( dff["freq"].unique() )
  for i in sorted( [str(fr) for fr in freqs] ):
    print(i)

for fn in filenames:
  print("\n\n" + fn)
  check(fn)
