import pandas as pd

subsample=100

enph = "data/enph-2017/recip-" + str(subsample) + "/"

if True: # load new files
  persona                      = pd.read_csv( enph + "Caracteristicas_generales_personas.csv" )
  gasto_articulo               = pd.read_csv( enph + "Gastos_menos_frecuentes_-_Articulos.csv" )
  gasto_medio                  = pd.read_csv( enph + "Gastos_menos_frecuentes_-_Medio_de_pago.csv" )
  gasto_rural_capitulo_c       = pd.read_csv( enph + "Gastos_semanales_Rural_-_Capitulo_C.csv" )
  gasto_urbano_capitulo_c      = pd.read_csv( enph + "Gastos_diarios_Urbano_-_Capitulo_C.csv" )
  # not (currently) VAT-relevant
    # vivienda                     = pd.read_csv( enph + "Viviendas_y_hogares.csv" )
    # gasto_rural_mercado          = pd.read_csv( enph + "Gastos_semanales_Rurales_-_Mercados.csv" )
    # gasto_urbano_mercado         = pd.read_csv( enph + "Gastos_diarios_Urbanos_-_Mercados.csv" )
  gasto_rural_personal         = pd.read_csv( enph + "Gastos_personales_Rural.csv" )
  gasto_rural_personal_fuera   = pd.read_csv( enph + "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar.csv" )
  gasto_rural_semanal          = pd.read_csv( enph + "Gastos_semanales_Rurales.csv" )
  gasto_rural_semanal_fuera    = pd.read_csv( enph + "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar.csv" )
  gasto_urbano_diario          = pd.read_csv( enph + "Gastos_diarios_Urbanos.csv" )
  gasto_urbano_diario_fuera    = pd.read_csv( enph + "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv" )
  gasto_urbano_diario_personal = pd.read_csv( enph + "Gastos_diarios_personales_Urbano.csv" )
  gasto_urbano_personal_fuera  = pd.read_csv( enph + "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv" )
