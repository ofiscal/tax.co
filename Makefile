SHELL := bash
.PHONY: \
  input_subsamples \
  buildings \
  people \
  vat_rates


##=##=##=##=##=##=##=## Variables

##=##=##=##  Non-file variables

subsample?=1 # default value; can be overridden from the command line, as in "make raw subsample=10"
             # valid values are 1, 10, 100 and 1000
ss=$(strip $(subsample))# removes trailing space
python_from_here = PYTHONPATH='.' python3


##=##=##=##  Input data variables

enph_files = \
  Caracteristicas_generales_personas \
  Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar \
  Gastos_diarios_personales_Urbano \
  Gastos_diarios_Urbano_-_Capitulo_C \
  Gastos_diarios_Urbanos \
  Gastos_diarios_Urbanos_-_Mercados \
  Gastos_menos_frecuentes_-_Articulos \
  Gastos_menos_frecuentes_-_Medio_de_pago \
  Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar \
  Gastos_personales_Rural \
  Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar \
  Gastos_semanales_Rural_-_Capitulo_C \
  Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar \
  Gastos_semanales_Rurales \
  Gastos_semanales_Rurales_-_Mercados \
  Viviendas_y_hogares

enph_orig = $(addsuffix .csv, $(addprefix data/enph-2017/orig/csv/, $(enph_files)))


##=##=##=##  Target variables

input_subsamples =                                                           \
  $(addsuffix .csv, $(addprefix data/enph-2017/recip-$(ss)/, $(enph_files)))

buildings = output/vat/data/recip-$(ss)/buildings.csv

people = output/vat/data/recip-$(ss)/people.csv

purchases = output/vat/data/recip-$(ss)/purchases.csv

vat_rates = output/vat/data/recip-$(ss)/vat_coicop.csv \
  output/vat/data/recip-$(ss)/vat_cap_c.csv


##=##=##=##=##=##=##=## Recipes

##=##=##=## subsample, or very slightly tweak, some input data sets

input_subsamples: $(input_subsamples)
$(input_subsamples) : python/subsample.py $(enph_orig)
	$(python_from_here) python/subsample.py

vat_rates: $(vat_rates)
$(vat_rates): python/vat/build/vat_rates.py \
  data/vat/vat-by-coicop.csv \
  data/vat/vat-for-capitulo-c.csv \
  python/vat/build/classes.py \
  python/vat/build/common.py \
  python/vat/build/output_io.py
	$(python_from_here) python/vat/build/vat_rates.py $(subsample)


##=##=##=## Build things from the ENPH

buildings: $(buildings)
$(buildings): $(input_subsamples) python/vat/build/buildings.py \
  python/vat/build/classes.py \
  python/vat/build/common.py \
  python/vat/build/output_io.py
	$(python_from_here) python/vat/build/buildings.py $(subsample)

people: $(people)
$(people): $(input_subsamples) python/vat/build/people/main.py \
  python/vat/build/classes.py \
  python/vat/build/people/files.py \
  python/vat/build/common.py \
  python/vat/build/output_io.py
	$(python_from_here) python/vat/build/people/main.py $(subsample)

purchases: $(purchases)
$(purchases): $(input_subsamples) python/vat/build/purchases/main.py \
  python/vat/build/purchases/nice_purchases.py \
  python/vat/build/purchases/medios.py \
  python/vat/build/purchases/articulos.py \
  python/vat/build/purchases/capitulo_c.py \
  python/vat/build/classes.py \
  python/vat/build/common.py \
  python/vat/build/output_io.py
	$(python_from_here) python/vat/build/purchases/main.py $(subsample)
