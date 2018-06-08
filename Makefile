SHELL := bash
.PHONY = raw

raw: $(enig_orig) $(enph_orig) $(subsamples)

enig_orig = $(addsuffix .txt, $(addprefix data/enig-2007/orig-txt/, $(enig_files)))
enph_orig = $(addsuffix .dta, $(addprefix data/enph-2017/orig-dta/, $(enph_files)))
subsamples = $(addsuffix .csv, $(addprefix data/enph-2017/recip-1/, $(enph_files)))      \
             $(addsuffix .csv, $(addprefix data/enig-2007/recip-1/, $(enig_files)))      \
             $(addsuffix .csv, $(addprefix data/enph-2017/recip-10/, $(enph_files)))     \
             $(addsuffix .csv, $(addprefix data/enig-2007/recip-10/, $(enig_files)))     \
             $(addsuffix .csv, $(addprefix data/enph-2017/recip-100/, $(enph_files)))    \
             $(addsuffix .csv, $(addprefix data/enig-2007/recip-100/, $(enig_files)))    \
             $(addsuffix .csv, $(addprefix data/enph-2017/recip-1000/, $(enph_files)))   \
             $(addsuffix .csv, $(addprefix data/enig-2007/recip-1000/, $(enig_files)))

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

enig_files = Ig_gsdp_dias_sem \
  Ig_gsdp_gas_dia \
  Ig_gsdp_perceptores \
  Ig_gsdu_caract_alim \
  Ig_gsdu_dias_sem \
  Ig_gsdu_gas_dia \
  Ig_gsdu_gasto_alimentos_cap_c \
  Ig_gsdu_mercado \
  Ig_gs_hogar \
  Ig_gsmf_compra \
  Ig_gsmf_forma_adqui \
  Ig_gsmf_serv_pub \
  Ig_gssr_caract_alim \
  Ig_gssr_gas_sem \
  Ig_gssr_gasto_alimentos_cap_c \
  Ig_gssr_mercado \
  Ig_gs_vivienda \
  Ig_ml_desocupado \
  Ig_ml_hogar \
  Ig_ml_inactivo \
  Ig_ml_ocupado \
  Ig_ml_pblcion_edad_trbjar \
  Ig_ml_persona \
  Ig_ml_vivienda


## ## Build the data for the VAT analysis


## ## Build every subsample of the ENPH and the ENIG

subsamples : python/subsample.py $(enig_orig) $(enph_orig)
	PYTHONPATH='.' python3 python/subsample.py


## ## Build the ENPH 2017

data/enph-2017/enph-2017.orig-dta.tgz:
	cd data;                               \
	  mkdir -p enph-2017;                  \
	  mv enph-2017.orig-dta.tgz enph-2017;

$(enph_orig): data/enph-2017/enph-2017.orig-dta.tgz
	cd data/enph-2017;                  \
	  tar -xvzf enph-2017.orig-dta.tgz; \
	  touch orig-dta/*.dta # without this the rule repeats itself


## ## Build the ENIG 2007

data/enig-2007/enig-2007.orig-txt.tgz:
	cd data;                               \
	  mkdir -p enig-2007;                  \
	  mv enig-2007.orig-txt.tgz enig-2007;

$(enig_orig): data/enig-2007/enig-2007.orig-txt.tgz
	cd data/enig-2007;                  \
	  tar -xvzf enig-2007.orig-txt.tgz; \
	  touch orig-txt/*.txt # without this the rule repeats itself
