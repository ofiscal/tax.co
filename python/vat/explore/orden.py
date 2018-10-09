# I found the range of household-member implausible (see check_orden.txt) so wrote this test to be sure
# I wasn't mangling the data.


# Checking all the ORDEN fields
import pandas as pd
import python.util as util

filenames = [
  "Caracteristicas_generales_personas.csv"
  , "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv"
  , "Gastos_diarios_personales_Urbano.csv"
  , "Gastos_diarios_Urbano_-_Capitulo_C.csv"
  , "Gastos_diarios_Urbanos.csv"
  , "Gastos_diarios_Urbanos_-_Mercados.csv"
  , "Gastos_menos_frecuentes_-_Articulos.csv"
  , "Gastos_menos_frecuentes_-_Medio_de_pago.csv"
  , "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar.csv"
  , "Gastos_personales_Rural.csv"
  , "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv"
  , "Gastos_semanales_Rural_-_Capitulo_C.csv"
  , "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar.csv"
  , "Gastos_semanales_Rurales.csv"
  , "Gastos_semanales_Rurales_-_Mercados.csv"
  , "Viviendas_y_hogares.csv"
]

def fetch(filename):
  x = pd.read_csv( "data/enph-2017/recip-100/" + filename
                   , usecols = ["ORDEN"] ).astype('int')
  return (filename,x)

name_datas = list( map( fetch, filenames ) )

for (name, data) in name_datas:
  print(name)
  print( util.describeWithMissing( data ) )
  print()
