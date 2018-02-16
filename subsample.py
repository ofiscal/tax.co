# At times this is memory intensive. My OS kept killing it, until I ran it with nothing else going on
# -- closed my browsers and all other docker containers. (I left Emacs, Dolphin and a few Konsoles open.)

import pandas as pd


## The 2017 ENIG survey

folder = "data/enig-2017/"
names = [ "coicop.dta"
          , "factores_ciclo19.dta"
          , "hogares_tot_completos.dta"
          , "st2_sea_enc_gcar_csv.dta"
          , "st2_sea_enc_gcau_csv.dta"
          , "st2_sea_enc_gcfhr_ce_csv.dta"
          , "st2_sea_enc_gcfhr_csv.dta"
          , "st2_sea_enc_gcfhu_diarios_csv.dta"
          , "st2_sea_enc_gcfhup_diarios_csv.dta"
          , "st2_sea_enc_gdr_csv.dta"
          , "st2_sea_enc_gdrj1_csv.dta"
          , "st2_sea_enc_gdsr_mer_csv.dta"
          , "st2_sea_enc_gdsu_mer_csv.dta"
          , "st2_sea_enc_gmf_csv.dta"
          , "st2_sea_enc_gmf_transpuesta.dta"
          , "st2_sea_enc_gsdp_dia_csv.dta"
          , "st2_sea_enc_gsdp_diarios_csv.dta"
          , "st2_sea_enc_gsdu_dia_csv.dta"
          , "st2_sea_enc_gsdu_diarios_csv.dta" # the biggest, 1.5GB; if this goes through, everything does
          , "st2_sea_enc_hogc3_csv.dta"
          , "st2_sea_enc_hog_csv.dta"
          , "st2_sea_enc_per_csv.dta"
]

for name in names:
  print("now (henceforth) processing: " + name)
  data = pd.read_stata(folder + "orig-dta/" + name)
  data_recip_10 =  data.sample(frac=0.1) 
  data_recip_10.to_csv(   folder + "recip-10/"   + name)
  data_recip_100 =  data.sample(frac=0.01) 
  data_recip_100.to_csv(  folder + "recip-100/"  + name)
  data_recip_1000 = data.sample(frac=0.001)
  data_recip_1000.to_csv( folder + "recip-1000/" + name)


## The 2007 ENIG survey

folder = "data/enig-2007/"
names = [   "Ig_gsdp_dias_sem.txt"
          , "Ig_gsdp_gas_dia.txt"
          , "Ig_gsdp_perceptores.txt"
          , "Ig_gsdu_caract_alim.txt"
          , "Ig_gsdu_dias_sem.txt"
          , "Ig_gsdu_gas_dia.txt"
          , "Ig_gsdu_gasto_alimentos_cap_c.txt"
          , "Ig_gsdu_mercado.txt"
          , "Ig_gs_hogar.txt"
          , "Ig_gsmf_compra.txt"
          , "Ig_gsmf_forma_adqui.txt"
          , "Ig_gsmf_serv_pub.txt"
          , "Ig_gssr_caract_alim.txt"
          , "Ig_gssr_gas_sem.txt"
          , "Ig_gssr_gasto_alimentos_cap_c.txt"
          , "Ig_gssr_mercado.txt"
          , "Ig_gs_vivienda.txt"
          , "Ig_ml_desocupado.txt"
          , "Ig_ml_hogar.txt"
          , "Ig_ml_inactivo.txt"
          , "Ig_ml_ocupado.txt"
          , "Ig_ml_pblcion_edad_trbjar.txt"
          , "Ig_ml_persona.txt"
          , "Ig_ml_vivienda.txt"
]

for name in names:
  print("now (henceforth) processing: " + name)
  dtype_dict = {}
  # for the logic behind the next two lines, see format-investigations.py
  if name == "Ig_ml_hogar.txt":                 dtype_dict = {'P5185S9A1': str}
  elif name == "Ig_ml_pblcion_edad_trbjar.txt": dtype_dict = {'P7580S1': str}
  data = pd.read_csv(     folder + "recip-1/" + name, sep='\t', encoding='latin_1', dtype = dtype_dict)
  data_recip_10 =  data.sample(frac=0.1) 
  data_recip_10.to_csv(   folder + "recip-10/"   + name)
  data_recip_100 =  data.sample(frac=0.01) 
  data_recip_100.to_csv(  folder + "recip-100/"  + name)
  data_recip_1000 = data.sample(frac=0.001)
  data_recip_1000.to_csv( folder + "recip-1000/" + name)
