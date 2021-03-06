# In retrospect this code looks prematurely optimized.
# Its intent is to make it more convenient to retrieve the raw data.
# But so far we don't even use the ENIG (the 2007 version of the ENPH),
# so this is more flexible than we need.

def yearSurveyFolder(year):
  if year in (2007,2017):
    if year == 2007: return "data/enig-2007/"
    elif year == 2017: return "data/enph-2017/"
  else: raise ValueError (str(year) + " is not one of the survey years.")

files = { # files in the ENPH (2017) and the ENIG (2007)
  2017: [ "Caracteristicas_generales_personas"
        , "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar"
        , "Gastos_diarios_personales_Urbano"
        , "Gastos_diarios_Urbanos"
        , "Gastos_diarios_Urbanos_-_Mercados"
        , "Gastos_diarios_Urbano_-_Capitulo_C"
        , "Gastos_menos_frecuentes_-_Articulos"
        , "Gastos_menos_frecuentes_-_Medio_de_pago"
        , "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar"
        , "Gastos_personales_Rural"
        , "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar"
        , "Gastos_semanales_Rural_-_Capitulo_C"
        , "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar"
        , "Gastos_semanales_Rurales"
        , "Gastos_semanales_Rurales_-_Mercados"
        , "Viviendas_y_hogares"
  ],

  2007: [ "Ig_gsdp_dias_sem"
        , "Ig_gsdp_gas_dia"
        , "Ig_gsdp_perceptores"
        , "Ig_gsdu_caract_alim"
        , "Ig_gsdu_dias_sem"
        , "Ig_gsdu_gas_dia"
        , "Ig_gsdu_gasto_alimentos_cap_c"
        , "Ig_gsdu_mercado"
        , "Ig_gs_hogar"
        , "Ig_gsmf_compra"
        , "Ig_gsmf_forma_adqui"
        , "Ig_gsmf_serv_pub"
        , "Ig_gssr_caract_alim"
        , "Ig_gssr_gas_sem"
        , "Ig_gssr_gasto_alimentos_cap_c"
        , "Ig_gssr_mercado"
        , "Ig_gs_vivienda"
        , "Ig_ml_desocupado"
        , "Ig_ml_hogar"
        , "Ig_ml_inactivo"
        , "Ig_ml_ocupado"
        , "Ig_ml_pblcion_edad_trbjar"
        , "Ig_ml_persona"
        , "Ig_ml_vivienda"
  ] }
