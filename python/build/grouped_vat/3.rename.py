if True:
  import pandas as pd
  import numpy as np
  import os
  import re # regex


folder = "config/vat/grouped/"
coicop_path = os.path.join ( folder, "vat_by_coicop.csv" )
cap_c_path = os.path.join ( folder, "vat_by_capitulo_c.csv" )


###
### Fix column names.
###

for path in [ coicop_path, cap_c_path ]:
  df = pd.read_csv ( path )
  df = df.rename (
    columns = {
      # PITFALL: This method doesn't work for some columns names
      # with special characters, which is why I use regular expressions too.
      "Estupefacientes"              : "estupefacientes",
      "Para hombres"                 : "para hombres",
      "medicamentos (medicina)"      : "medicamentos",
      "impuestos saludables (bienes" : "impuestos saludables",
      "description"                  : "DESCRIPTION",
    } )
  df = df.rename (
    columns = lambda x: re.sub (
      ".*exclusivo para mujeres.*", "used only by females", x ) )
  df = df.rename (
    columns = lambda x: re.sub (
      ".*infantiles.*", "infantiles", x ) )
  df = df.rename (
    columns = lambda x: re.sub (
      ".*Rol de g.*fem.*", "female gender role", x ) )
  df = df.rename (
    columns = lambda x: re.sub (
      ".*veh.*culo.*", "vehículos", x ) )
  df.to_csv ( path,
              index = False )
