import pandas as pd

folders = ["data/enig-2017/"]
names = [ # "coicop.dta"
          # , "factores_ciclo19.dta"
          # , "hogares_tot_completos.dta"
          # , "st2_sea_enc_gcar_csv.dta"
          # , "st2_sea_enc_gcau_csv.dta"
          # , "st2_sea_enc_gcfhr_ce_csv.dta"
          # , "st2_sea_enc_gcfhr_csv.dta"
          # , "st2_sea_enc_gcfhu_diarios_csv.dta"
          # , "st2_sea_enc_gcfhup_diarios_csv.dta"
          # , "st2_sea_enc_gdr_csv.dta"
          # , "st2_sea_enc_gdrj1_csv.dta"
          # , "st2_sea_enc_gdsr_mer_csv.dta"
          # , "st2_sea_enc_gdsu_mer_csv.dta"
          # , "st2_sea_enc_gmf_csv.dta"
          # , "st2_sea_enc_gmf_transpuesta.dta"
          # , "st2_sea_enc_gsdu_dia_csv.dta"
          "st2_sea_enc_gsdp_diarios_csv.dta" # TODO : this one's huge, killing the process
          , "st2_sea_enc_gsdu_dia_csv.dta"
          , "st2_sea_enc_gsdu_diarios_csv.dta"
          , "st2_sea_enc_hogc3_csv.dta"
          , "st2_sea_enc_hog_csv.dta"
          , "st2_sea_enc_per_csv.dta"
]

for folder in folders:
  for name in names:
    data = pd.read_stata(folder + "orig-dta/" + name)
    data_recip_10 =  data.sample(frac=0.1) 
    data_recip_10.to_csv(   folder + "recip-10/"   + name)
    data_recip_100 =  data.sample(frac=0.01) 
    data_recip_100.to_csv(  folder + "recip-100/"  + name)
    data_recip_1000 = data.sample(frac=0.001)
    data_recip_1000.to_csv( folder + "recip-1000/" + name)

list(data.columns.values)
