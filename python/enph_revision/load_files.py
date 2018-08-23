import pandas as pd
import python.enph_compare_official_to_pre_release.files as filetree
import numpy as np

coicop_vat = pd.read_csv( "data/vat/coicop-vat.csv", sep=';' )

if True: # old files
  coicop                 = pd.read_csv( filetree.old_folder + "coicop.csv")
  factores_ciclo19       = pd.read_csv( filetree.old_folder + "factores_ciclo19.csv")
  hogares_tot_completos  = pd.read_csv( filetree.old_folder + "hogares_tot_completos.csv")
  gcar                   = pd.read_csv( filetree.old_folder + "st2_sea_enc_gcar_csv.csv")
  gcau                   = pd.read_csv( filetree.old_folder + "st2_sea_enc_gcau_csv.csv")
  gcfhr_ce               = pd.read_csv( filetree.old_folder + "st2_sea_enc_gcfhr_ce_csv.csv")
  gcfhr                  = pd.read_csv( filetree.old_folder + "st2_sea_enc_gcfhr_csv.csv")
  gcfhu_diarios          = pd.read_csv( filetree.old_folder + "st2_sea_enc_gcfhu_diarios_csv.csv")
  gcfhup_diarios         = pd.read_csv( filetree.old_folder + "st2_sea_enc_gcfhup_diarios_csv.csv")
  gdr                    = pd.read_csv( filetree.old_folder + "st2_sea_enc_gdr_csv.csv")
  gdrj1                  = pd.read_csv( filetree.old_folder + "st2_sea_enc_gdrj1_csv.csv")
  gdsr_mer               = pd.read_csv( filetree.old_folder + "st2_sea_enc_gdsr_mer_csv.csv")
  gdsu_mer               = pd.read_csv( filetree.old_folder + "st2_sea_enc_gdsu_mer_csv.csv")
  gmf                    = pd.read_csv( filetree.old_folder + "st2_sea_enc_gmf_csv.csv")
  gmf_transpuesta        = pd.read_csv( filetree.old_folder + "st2_sea_enc_gmf_transpuesta.csv")
  gsdp_dia               = pd.read_csv( filetree.old_folder + "st2_sea_enc_gsdp_dia_csv.csv")
  gsdp_diarios           = pd.read_csv( filetree.old_folder + "st2_sea_enc_gsdp_diarios_csv.csv")
  gsdu_dia               = pd.read_csv( filetree.old_folder + "st2_sea_enc_gsdu_dia_csv.csv")
  gsdu_diarios           = pd.read_csv( filetree.old_folder + "st2_sea_enc_gsdu_diarios_csv.csv")
  hogc3                  = pd.read_csv( filetree.old_folder + "st2_sea_enc_hogc3_csv.csv")
  hog                    = pd.read_csv( filetree.old_folder + "st2_sea_enc_hog_csv.csv")
  per                    = pd.read_csv( filetree.old_folder + "st2_sea_enc_per_csv.csv")


if True: # new files
  caracteristicas_generales_personas                 = pd.read_csv( filetree.new_folder + "Caracteristicas_generales_personas.csv")
  gastos_diarios_urbano__comidas_preparadas_fuera    = pd.read_csv( filetree.new_folder + "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv")
  gastos_diarios_personales_urbano                   = pd.read_csv( filetree.new_folder + "Gastos_diarios_personales_Urbano.csv")
  gastos_diarios_urbanos                             = pd.read_csv( filetree.new_folder + "Gastos_diarios_Urbanos.csv")
  gastos_diarios_urbanos__mercados                   = pd.read_csv( filetree.new_folder + "Gastos_diarios_Urbanos_-_Mercados.csv")
  gastos_menos_frecuentes__articulos                 = pd.read_csv( filetree.new_folder + "Gastos_menos_frecuentes_-_Articulos.csv")
  gastos_menos_frecuentes__medio_de_pago             = pd.read_csv( filetree.new_folder + "Gastos_menos_frecuentes_-_Medio_de_pago.csv")
  gastos_personales_rural__comidas_preparadas_fuera  = pd.read_csv( filetree.new_folder + "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar.csv")
  gastos_personales_rural                            = pd.read_csv( filetree.new_folder + "Gastos_personales_Rural.csv")
  gastos_personales_urbano__comidas_preparadas_fuera = pd.read_csv( filetree.new_folder + "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv")
  gastos_semanales_rural__capitulo_c                 = pd.read_csv( filetree.new_folder + "Gastos_semanales_Rural_-_Capitulo_C.csv")
  gastos_semanales_rural__comidas_preparadas_fuera   = pd.read_csv( filetree.new_folder + "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar.csv")
  gastos_semanales_rurales                           = pd.read_csv( filetree.new_folder + "Gastos_semanales_Rurales.csv")
  gastos_semanales_rurales__mercados                 = pd.read_csv( filetree.new_folder + "Gastos_semanales_Rurales_-_Mercados.csv")
  viviendas_y_hogares                                = pd.read_csv( filetree.new_folder + "Viviendas_y_hogares.csv")

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

