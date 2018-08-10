.PHONY: raw_data

##=##=##=## Variables

enph_files = coicop              \
  factores_ciclo19               \
  hogares_tot_completos          \
  st2_sea_enc_gcar_csv           \
  st2_sea_enc_gcau_csv           \
  st2_sea_enc_gcfhr_ce_csv       \
  st2_sea_enc_gcfhr_csv          \
  st2_sea_enc_gcfhu_diarios_csv  \
  st2_sea_enc_gcfhup_diarios_csv \
  st2_sea_enc_gdr_csv            \
  st2_sea_enc_gdrj1_csv          \
  st2_sea_enc_gdsr_mer_csv       \
  st2_sea_enc_gdsu_mer_csv       \
  st2_sea_enc_gmf_csv            \
  st2_sea_enc_gmf_transpuesta    \
  st2_sea_enc_gsdp_dia_csv       \
  st2_sea_enc_gsdp_diarios_csv   \
  st2_sea_enc_gsdu_dia_csv       \
  st2_sea_enc_gsdu_diarios_csv   \
  st2_sea_enc_hogc3_csv          \
  st2_sea_enc_hog_csv            \
  st2_sea_enc_per_csv

enph_orig = $(addsuffix .dta, $(addprefix enph-2017/orig-dta/, $(enph_files)))


##=##=##=## Recipes

raw_data: $(enph_orig) vat/coicop-vat.csv

vat/coicop-vat.csv:
	mkdir -p vat
	mv coicop-vat.csv vat


##=## Build the ENPH 2017

enph-2017/enph-2017.orig-dta.tgz:
	mkdir -p enph-2017
	mv enph-2017.orig-dta.tgz enph-2017

$(enph_orig): enph-2017/enph-2017.orig-dta.tgz
	cd enph-2017;                       \
	  tar -xvzf enph-2017.orig-dta.tgz; \
	  touch orig-dta/*.dta  # else the rule repeats itself
