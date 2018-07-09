SHELL := bash
.PHONY: input_subsamples      \
  vat_data                    \
  vat_pics                    \
  vat_pics_households         \
  vat_pics_income-households  \
  vat_pics_people             \
  vat_pics_purchases          \
  vat_tables                  \
  vat_pdf


##=##=##=##=##=##=##=## Variables

##=## Non-target variables

subsample?=1 # default value; can be overridden from the command line, as in "make raw subsamples=10"
             # valid values are 1, 10, 100 and 1000
ss=$(strip $(subsample))# removes trailing space
python_from_here = PYTHONPATH='.' python3


##=##=##=## Variables: ENIG, ENPH and subsamples

# pitfall: the _csv suffix on these filenames is not a file extension
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

enig_files = Ig_gsdp_dias_sem    \
  Ig_gsdp_gas_dia                \
  Ig_gsdp_perceptores            \
  Ig_gsdu_caract_alim            \
  Ig_gsdu_dias_sem               \
  Ig_gsdu_gas_dia                \
  Ig_gsdu_gasto_alimentos_cap_c  \
  Ig_gsdu_mercado                \
  Ig_gs_hogar                    \
  Ig_gsmf_compra                 \
  Ig_gsmf_forma_adqui            \
  Ig_gsmf_serv_pub               \
  Ig_gssr_caract_alim            \
  Ig_gssr_gas_sem                \
  Ig_gssr_gasto_alimentos_cap_c  \
  Ig_gssr_mercado                \
  Ig_gs_vivienda                 \
  Ig_ml_desocupado               \
  Ig_ml_hogar                    \
  Ig_ml_inactivo                 \
  Ig_ml_ocupado                  \
  Ig_ml_pblcion_edad_trbjar      \
  Ig_ml_persona                  \
  Ig_ml_vivienda

enig_orig = $(addsuffix .txt, $(addprefix data/enig-2007/orig-txt/, $(enig_files)))
enph_orig = $(addsuffix .dta, $(addprefix data/enph-2017/orig-dta/, $(enph_files)))
input_subsamples =                                                           \
  $(addsuffix .csv, $(addprefix data/enph-2017/recip-$(ss)/, $(enph_files))) \
  $(addsuffix .csv, $(addprefix data/enig-2007/recip-$(ss)/, $(enig_files)))


##=##=##=## Variables: VAT tables and pictures

vat_tables_rootless = income-by-income-decile.tex \
  vat-over-spending-by-income-decile.tex
vat_tables  = $(addprefix output/vat-tables/recip-$(ss)/,  $(vat_tables_rootless))

vat_pics_rootless =                      \
  $(vat_pics_households_rootless)        \
  $(vat_pics_income-households_rootless) \
  $(vat_pics_people_rootless)            \
  $(vat_pics_purchases_rootless)
vat_pics_households_rootless = households/oldest.png       \
  households/transactions-per-month.png                    \
  households/youngest.png                                  \
  households/size.png                                      \
  households/max-edu.png                                   \
  households/VAT-over-consumption,-by-income-decile.png    \
  households/income.png
vat_pics_income-households_rootless =                      \
  income-households/VAT-over-income,-by-has-elderly.png    \
  income-households/VAT-over-income,-by-has-child.png      \
  income-households/spending-over-income.png               \
  income-households/VAT-over-income,-by-income-decile.png
vat_pics_people_rootless =                                 \
  people/transactions-per-month.png                        \
  people/spending-per-month.png                            \
  people/age.png                                           \
  people/education.png                                     \
  people/income.png
vat_pics_purchases_rootless = purchases/value.png          \
  purchases/frequency.png                                  \
  purchases/quantity.png                                   \
  purchases/vat-in-pesos.png

vat_pics_households = \
  $(addprefix output/vat-pics/recip-$(ss)/, $(vat_pics_households_rootless))
vat_pics_income-households = \
  $(addprefix output/vat-pics/recip-$(ss)/, $(vat_pics_income-households_rootless))
vat_pics_people    = \
  $(addprefix output/vat-pics/recip-$(ss)/, $(vat_pics_people_rootless))
vat_pics_purchases = \
  $(addprefix output/vat-pics/recip-$(ss)/, $(vat_pics_purchases_rootless))
vat_pics = $(vat_pics_households) $(vat_pics_income-households) $(vat_pics_people) $(vat_pics_purchases)


##=##=##=## Variables: VAT datasets

# The VAT data build is divided into two stages:
  # "early" (big, slow, hopefully infrequent) and "late"

vat_files = $(vat_files_early) $(vat_files_late)
vat_files_early = 1.purchases.csv                \
  2.purchases,prices,taxes.csv
vat_files_late = 3.person-level-expenditures.csv \
  4.demog.csv                                    \
  5.person-demog-expenditures.csv                \
  6.households.csv                               \
  7.households_w_income.csv                      \
  8.households_w_income_decile_summary.csv       \
  9.households_decile_summary.csv


##=##=##=## Variables: More

vat_pdf = tex/recip-$(ss)/vat.pdf

vat_data = $(addprefix output/vat-data/recip-$(ss)/, $(vat_files))
vat_data_early = $(addprefix output/vat-data/recip-$(ss)/,    $(vat_files_early))
vat_data_late  = $(addprefix output/vat-data/recip-$(ss)/,    $(vat_files_late))


##=##=##=##=##=##=##=## Recipes

##=##=##=## Create the PDF of the VAT analysis

# this runs pdflatex twice; the first defines references used in the second
vat_pdf: $(vat_pdf)
$(vat_pdf): tex/vat.tex $(vat_pics) $(vat_tables)
	cd tex;                                                 \
	  mkdir -p recip-$(ss);                                 \
	  for i in 1 2; do                                      \
	    pdflatex -output-directory recip-$(ss)              \
              "\newcommand\subsample[0]{$(ss)}\input{vat.tex}"; \
	  done


##=##=##=## Create TeX figures for the VAT analysis

vat_pics: $(vat_pics)
vat_tables: $(vat_tables)

vat_pics_households: $(vat_pics_households)
$(vat_pics_households) $(vat_tables): $(vat_data)     \
  python/draw/shell-load.py                           \
  python/draw/util.py                                 \
  python/vat/report/main,households.py                \
  python/vat/report/load.py                           \
  python/vat/report/pics,households.py
	$(python_from_here) python/vat/report/main,households.py $(ss)

vat_pics_income-households: $(vat_pics_income-households)
$(vat_pics_income-households): $(vat_data)         \
  python/draw/shell-load.py                        \
  python/draw/util.py                              \
  python/vat/report/main,income-households.py      \
  python/vat/report/load.py                        \
  python/vat/report/pics,income-households.py
	$(python_from_here) python/vat/report/main,income-households.py $(ss)

vat_pics_people: $(vat_pics_people)
$(vat_pics_people): $(vat_data)        \
  python/draw/shell-load.py            \
  python/draw/util.py                  \
  python/vat/report/main,people.py     \
  python/vat/report/load.py            \
  python/vat/report/pics,people.py
	$(python_from_here) python/vat/report/main,people.py $(ss)

vat_pics_purchases: $(vat_pics_purchases)
$(vat_pics_purchases): $(vat_data)     \
  python/draw/shell-load.py            \
  python/draw/util.py                  \
  python/vat/report/main,purchases.py  \
  python/vat/report/load.py            \
  python/vat/report/pics,purchases.py
	$(python_from_here) python/vat/report/main,purchases.py $(ss)


##=##=##=## Build the data for the VAT analysis

vat_data: $(vat_data_early) $(vat_data_late)
$(vat_data_early): $(input_subsamples) python/vat/build_early.py
	$(python_from_here) python/vat/build_early.py $(subsample)
$(vat_data_late): $(vat_data_early) python/vat/build_late.py
	$(python_from_here) python/vat/build_late.py $(subsample)


##=##=##=## Build subsamples ofthe ENPH and the ENIG

input_subsamples: $(input_subsamples)
# TODO ? rather than build these monolithically, make the subsample size a parameter of subsample.py
  # would be faster if, e.g., you wanted to build only the 1/1000 subsample and not the others
  # but on the other hand building every subsample would require loading the input four times
$(input_subsamples) : $(enig_orig) $(enph_orig)
  # TODO ? add python/subsample.py to dependencies
	$(python_from_here) python/subsample.py
