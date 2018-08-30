# this needs the variable "subsample" to be defined, as either 1, 10, 100 or 1000

import os


try: subsample
except NameError: subsample = 100


output_folder = "output/enph_revision/"
if not os.path.exists(output_folder): os.makedirs(output_folder)

old_folder = "data/enph-2017/pre-publication/recip-" + str(subsample) + "/"

new_folder = "data/enph-2017/recip-" + str(subsample) + "/"

old_file_names = [ "coicop"
            , "factores_ciclo19"
            , "hogares_tot_completos"
            , "st2_sea_enc_gcar_csv"
            , "st2_sea_enc_gcau_csv"
            , "st2_sea_enc_gcfhr_ce_csv"
            , "st2_sea_enc_gcfhr_csv"
            , "st2_sea_enc_gcfhu_diarios_csv"
            , "st2_sea_enc_gcfhup_diarios_csv"
            , "st2_sea_enc_gdr_csv"
            , "st2_sea_enc_gdrj1_csv"
            , "st2_sea_enc_gdsr_mer_csv"
            , "st2_sea_enc_gdsu_mer_csv"
            , "st2_sea_enc_gmf_csv"
            , "st2_sea_enc_gmf_transpuesta"
            , "st2_sea_enc_gsdp_dia_csv"
            , "st2_sea_enc_gsdp_diarios_csv"
            , "st2_sea_enc_gsdu_dia_csv"
            , "st2_sea_enc_gsdu_diarios_csv"
            , "st2_sea_enc_hogc3_csv"
            , "st2_sea_enc_hog_csv"
            , "st2_sea_enc_per_csv"
            ]

new_file_names = [ "Caracteristicas_generales_personas"
            , "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar"
            , "Gastos_diarios_personales_Urbano"
            , "Gastos_diarios_Urbanos"
            , "Gastos_diarios_Urbanos_-_Mercados"
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
            ]
