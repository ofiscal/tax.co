SHELL := bash
.PHONY: input_subsamples \
  buildings \
  households \
  people_1 \
  people_2_buildings \
  people_3_purchases \
  purchases_1 \
  purchases_2_vat \
  purchase_sums \
  vat_rates \
  pics \
  purchase_pics \
  people_pics \
  household_pics \
  overview


##=##=##=##=##=##=##=## Variables

##=##=##=##  Non-file variables

subsample?=1
  # default value; can be overridden from the command line, as in "make raw subsample=10"
  # valid values are 1, 10, 100 and 1000
ss=$(strip $(subsample))# removes trailing space
vat_strategy?=approx
  # default value; can be overridden from command line, ala "make raw vat_strategy=detail"
s_vat_strategy=$(strip $(vat_strategy))# removes trailing space
vat_const_rate?=""# default value
s_vat_const_rate=$(patsubst "%",%,$(strip $(vat_const_rate)))
  # removes trailing space and "s
strategy_suffix=$(strip $(s_vat_strategy)_$(s_vat_const_rate))

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

buildings =          output/vat/data/recip-$(ss)/buildings.csv
households =         output/vat/data/recip-$(ss)/households.csv \
                     output/vat/data/recip-$(ss)/households_w_income.csv \
                     output/vat/data/recip-$(ss)/households_w_income_decile_summary.csv \
                     output/vat/data/recip-$(ss)/households_decile_summary.csv
people_1 =           output/vat/data/recip-$(ss)/people_1.csv
people_2_buildings = output/vat/data/recip-$(ss)/people_2_buildings.csv
people_3_purchases = output/vat/data/recip-$(ss)/people_3_purchases.csv
purchases_1 =        output/vat/data/recip-$(ss)/purchases_1.csv \
                     output/vat/data/recip-$(ss)/purchases_1_5_no_origin
purchases_2_vat =    output/vat/data/recip-$(ss)/purchases_2_vat.csv
purchase_sums =      output/vat/data/recip-$(ss)/purchase_sums.csv
vat_rates = \
  output/vat/data/recip-$(ss)/vat_coicop_$(strategy_suffix).csv \
  output/vat/data/recip-$(ss)/vat_cap_c_$(strategy_suffix).csv \
  output/vat/data/recip-$(ss)/vat_coicop_brief_$(strategy_suffix).csv \
  output/vat/data/recip-$(ss)/vat_cap_c_brief_$(strategy_suffix).csv

purchase_pics =      output/vat/pics/recip-$(ss)/purchases/frequency.png \
                     output/vat/pics/recip-$(ss)/purchases/quantity.png \
                     output/vat/pics/recip-$(ss)/purchases/value.png \
                     output/vat/pics/recip-$(ss)/purchases/vat-in-pesos,max.png \
                     output/vat/pics/recip-$(ss)/purchases/vat-in-pesos,min.png \
                     output/vat/pics/recip-$(ss)/purchases/logx/quantity.png \
                     output/vat/pics/recip-$(ss)/purchases/logx/value.png \
                     output/vat/pics/recip-$(ss)/purchases/logx/vat-in-pesos,max.png \
                     output/vat/pics/recip-$(ss)/purchases/logx/vat-in-pesos,min.png

people_pics = \
  output/vat/pics/recip-$(ss)/people/age.png \
  output/vat/pics/recip-$(ss)/people/education.png \
  output/vat/pics/recip-$(ss)/people/income,by-age-decile.png \
  output/vat/pics/recip-$(ss)/people/income.png \
  output/vat/pics/recip-$(ss)/people/spending-per-month.png \
  output/vat/pics/recip-$(ss)/people/transactions-per-month.png \
  output/vat/pics/recip-$(ss)/people/logx/income,by-age-decile.png \
  output/vat/pics/recip-$(ss)/people/logx/income.png \
  output/vat/pics/recip-$(ss)/people/logx/spending-per-month.png

household_pics = \
  output/vat/pics/recip-$(ss)/households/income.png \
  output/vat/pics/recip-$(ss)/households/logx/income.png \
  output/vat/pics/recip-$(ss)/households/max-edu.png \
  output/vat/pics/recip-$(ss)/households/oldest.png \
  output/vat/pics/recip-$(ss)/households/size.png \
  output/vat/pics/recip-$(ss)/households/transactions-per-month.png \
  output/vat/pics/recip-$(ss)/households/VAT-over-consumption,-by-income-decile.png \
  output/vat/pics/recip-$(ss)/households/youngest.png

pics = $(purchase_pics) $(people_pics) $(household_pics)

overview = output/vat/tables/recip-$(ss)/overview.csv


##=##=##=##=##=##=##=## Recipes

##=##=##=## subsample, or very slightly tweak, some input data sets

input_subsamples: $(input_subsamples)
$(input_subsamples): python/subsample.py $(enph_orig)
	$(python_from_here) python/subsample.py

vat_rates: $(vat_rates)
$(vat_rates): python/vat/build/vat_rates.py \
  python/vat/build/output_io.py \
  data/vat/vat-by-coicop.csv \
  data/vat/vat-for-capitulo-c.csv
	$(python_from_here) python/vat/build/vat_rates.py $(subsample) $(vat_strategy) $(vat_const_rate)


##=##=##=## Build data from the ENPH

buildings: $(buildings)
$(buildings): python/vat/build/buildings.py \
  python/vat/build/classes.py \
  python/vat/build/common.py \
  python/vat/build/output_io.py \
  $(input_subsamples)
	$(python_from_here) python/vat/build/buildings.py $(subsample) $(vat_strategy) $(vat_const_rate)

households: $(households)
$(households): python/vat/build/households.py \
  python/util.py \
  python/vat/build/output_io.py \
  $(people_3_purchases)
	$(python_from_here) python/vat/build/households.py $(subsample) $(vat_strategy) $(vat_const_rate)

people_1: $(people_1)
$(people_1): python/vat/build/people/main.py \
  python/vat/build/people/files.py \
  python/vat/build/common.py \
  python/vat/build/output_io.py \
  $(input_subsamples)
	$(python_from_here) python/vat/build/people/main.py $(subsample) $(vat_strategy) $(vat_const_rate)

people_2_buildings: $(people_2_buildings)
$(people_2_buildings): python/vat/build/people_2_buildings.py \
  python/vat/build/output_io.py \
  $(buildings) $(people_1)
	$(python_from_here) python/vat/build/people_2_buildings.py $(subsample) $(vat_strategy) $(vat_const_rate)

people_3_purchases: $(people_3_purchases)
$(people_3_purchases): python/vat/build/people_3_purchases.py \
  python/vat/build/output_io.py \
  $(people_2_buildings) $(purchase_sums)
	$(python_from_here) python/vat/build/people_3_purchases.py $(subsample) $(vat_strategy) $(vat_const_rate)

purchases_1: $(purchases_1)
$(purchases_1): python/vat/build/purchases/main.py \
  python/vat/build/classes.py \
  python/vat/build/common.py \
  python/vat/build/output_io.py \
  python/vat/build/purchases/nice_purchases.py \
  python/vat/build/purchases/medios.py \
  python/vat/build/purchases/articulos.py \
  python/vat/build/purchases/capitulo_c.py \
  $(input_subsamples)
	$(python_from_here) python/vat/build/purchases/main.py $(subsample) $(vat_strategy) $(vat_const_rate)

purchases_2_vat: $(purchases_2_vat)
$(purchases_2_vat): python/vat/build/purchases_2_vat.py \
  python/vat/build/output_io.py \
  python/vat/build/legends.py \
  $(vat_rates) \
  output/vat/data/recip-$(ss)/purchases_1.csv
	$(python_from_here) python/vat/build/purchases_2_vat.py $(subsample) $(vat_strategy) $(vat_const_rate)

purchase_sums: $(purchase_sums)
$(purchase_sums): python/vat/build/purchase_sums.py \
  python/vat/build/output_io.py \
  $(purchases_2_vat)
	$(python_from_here) python/vat/build/purchase_sums.py $(subsample) $(vat_strategy) $(vat_const_rate)


##=##=##=## Make charts, diagrams, tiny latex tables

purchase_pics: $(purchase_pics)
$(purchase_pics): python/vat/report/pics/purchases.py \
  $(purchases_2_vat)
	$(python_from_here) python/vat/report/pics/purchases.py $(subsample) $(vat_strategy) $(vat_const_rate)

household_pics: $(household_pics)
$(household_pics): python/vat/report/pics/households.py \
  $(households)
	$(python_from_here) python/vat/report/pics/households.py $(subsample) $(vat_strategy) $(vat_const_rate)

people_pics: $(people_pics)
$(people_pics): python/vat/report/pics/people.py \
  $(people_3_purchases)
	$(python_from_here) python/vat/report/pics/people.py $(subsample) $(vat_strategy) $(vat_const_rate)

pics: $(pics)

overview: $(overview)
$(overview): python/vat/report/tables/overview.py \
  python/util.py \
  python/vat/build/output_io.py \
  python/vat/build/people/files.py \
  $(households)
	$(python_from_here) python/vat/report/tables/overview.py $(subsample) $(vat_strategy) $(vat_const_rate)
