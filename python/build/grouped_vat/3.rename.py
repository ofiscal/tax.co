if True:
  import pandas as pd
  import numpy as np
  import os
  import re # regex


folder = "config/vat/grouped/"
raw = os.path.join ( folder, "1.dos2unix" )

coicop_path = os.path.join ( folder, "vat_by_coicop.csv" )
cap_c_path  = os.path.join ( folder, "vat_by_capitulo_c.csv" )
dicc_path   = os.path.join ( raw,    "dicc_coicop.tsv" )


###
### Fix column names.
###

simple_replacements = {
  # PITFALL: This method doesn't work for some columns names
  # with special characters, which is why I use regular expressions too.
  "Estupefacientes"              : "estupefacientes",

  # PITFALL: The order of the next two pairs might mnatter.
  "Para hombres"                 : "para hombres",
  "Para hombre"                  : "para hombres",

  "medicamentos (medicina)"      : "medicamentos",
  "impuestos saludables (bienes" : "impuestos saludables",
  "description"                  : "DESCRIPTION", }

regex_replacements = [
  ( ".*no saludables.*"          , "no saludable"         ),
  ( ".*perjudicial.*ambient.*"   , "daña el ambiente"     ),
  ( ".*exclusivo para mujeres.*" , "used only by females" ),
  ( ".*infantiles.*"             , "infantiles"           ),
  ( ".*Rol de g.*fem.*"          , "female gender role"   ),
  ( ".*veh.*culo.*"              , "vehículos"            ),
]

for path in [ coicop_path, cap_c_path ]:
  df = pd.read_csv ( path )
  df = df.rename ( columns = simple_replacements )
  for [before, after] in regex_replacements:
    df = df.rename (
      columns = lambda x: re.sub (
        before, after, x ) )
  df.to_csv ( path, index = False )


###
### Fix the same strings where they appear as cells
### (rather than column names).
###

dicc = pd.read_csv (
  "config/vat/grouped/1.dos2unix/dicc_coicop.tsv",
  sep = "\t" )

x = (
    regex_replacements
    + [ (k, v) for k, v
        in simple_replacements . items () ] )

# for (k,v) in simple_replacements . items ():
dicc["category"] = ( dicc["category"]
                     . replace( simple_replacements ) )

for [before, after] in regex_replacements:
  dicc["category"] = dicc["category"].apply (
    lambda x: re.sub (
      before, after, x ) )

dicc.to_csv (
  "config/vat/grouped/dicc_coicop.csv",
  index = False )
