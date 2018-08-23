newEnphsDfs = [ caracteristicas_generales_personas
              , gastos_diarios_urbano__comidas_preparadas_fuera
              , gastos_diarios_personales_urbano
              , gastos_diarios_urbanos
              , gastos_diarios_urbanos__mercados
              , gastos_menos_frecuentes__articulos
              , gastos_menos_frecuentes__medio_de_pago
              , gastos_personales_rural__comidas_preparadas_fuera
              , gastos_personales_rural
              , gastos_personales_urbano__comidas_preparadas_fuera
              , gastos_semanales_rural__capitulo_c
              , gastos_semanales_rural__comidas_preparadas_fuera
              , gastos_semanales_rurales
              , gastos_semanales_rurales__mercados
              , viviendas_y_hogares ]

for df in newEnphsDfs:
  df.columns = map(str.lower, df.columns)

gastos_semanales_rural__comidas_preparadas_fuera[  "nh_cgprcfh_p2"] = (
  gastos_semanales_rural__comidas_preparadas_fuera["nh_cgprcfh_p2"].replace(",1","1") )

gastos_diarios_urbano__comidas_preparadas_fuera[  "nh_cgducfh_p2"] = (
  gastos_diarios_urbano__comidas_preparadas_fuera["nh_cgducfh_p2"].replace(
    { ",5":5, ",25":25 } ) )

gastos_personales_urbano__comidas_preparadas_fuera[  "nh_cgpucfh_p2"] = (
  gastos_personales_urbano__comidas_preparadas_fuera["nh_cgpucfh_p2"].replace(
    {  ",1":1
       , ",25":25
       , ",5":5
       , "1,4":14
       , "1,5":15 } ) )

# PITFALL: This replaces 1% of all values
gastos_diarios_personales_urbano["nc4_cc_p2"] = (
  gastos_diarios_personales_urbano["nc4_cc_p2"].str.replace( ",", "") )

for df in newEnphsDfs:
  for c in df.columns:
    if df[c].dtype == 'O':
      df[c] = df[c].str.strip()
      df[c] = df[c].replace("", np.nan)
      df[c] = pd.to_numeric( df[c]
                           , errors='ignore' ) # ignore operation if any value won't convert
