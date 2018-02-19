prefix=data/enig-2017
subsampleFolders="recip-10 recip-100 recip-1000"
files="coicop
factores_ciclo19
hogares_tot_completos
st2_sea_enc_gcar_csv
st2_sea_enc_gcau_csv
st2_sea_enc_gcfhr_ce_csv
st2_sea_enc_gcfhr_csv
st2_sea_enc_gcfhu_diarios_csv
st2_sea_enc_gcfhup_diarios_csv
st2_sea_enc_gdr_csv
st2_sea_enc_gdrj1_csv
st2_sea_enc_gdsr_mer_csv
st2_sea_enc_gdsu_mer_csv
st2_sea_enc_gmf_csv
st2_sea_enc_gmf_transpuesta
st2_sea_enc_gsdp_dia_csv
st2_sea_enc_gsdp_diarios_csv
st2_sea_enc_gsdu_dia_csv
st2_sea_enc_gsdu_diarios_csv
st2_sea_enc_hogc3_csv
st2_sea_enc_hog_csv
st2_sea_enc_per_csv"

for s in $subsampleFolders
do for f in $files
   do mv $prefix/$s/$f.dta $prefix/$s/$f.csv
   done
done
