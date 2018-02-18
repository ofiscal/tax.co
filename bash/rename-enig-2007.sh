prefix=data/enig-2007
subsampleFolders="recip-10 recip-100 recip-1000"
files="Ig_gsdp_dias_sem
  Ig_gsdp_gas_dia
  Ig_gsdp_perceptores
  Ig_gsdu_caract_alim
  Ig_gsdu_dias_sem
  Ig_gsdu_gas_dia
  Ig_gsdu_gasto_alimentos_cap_c
  Ig_gsdu_mercado
  Ig_gs_hogar
  Ig_gsmf_compra
  Ig_gsmf_forma_adqui
  Ig_gsmf_serv_pub
  Ig_gssr_caract_alim
  Ig_gssr_gas_sem
  Ig_gssr_gasto_alimentos_cap_c
  Ig_gssr_mercado
  Ig_gs_vivienda
  Ig_ml_desocupado
  Ig_ml_hogar
  Ig_ml_inactivo
  Ig_ml_ocupado
  Ig_ml_pblcion_edad_trbjar
  Ig_ml_persona
  Ig_ml_vivienda"

for s in $subsampleFolders
do for f in $files
   do
       mv $prefix/$s/$f.txt $prefix/$s/$f.csv
   done
done
