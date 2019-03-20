# PITFALL: vat_flat_rate must only be specified (when calling make from the command line)
# if using a strategy wherein it can vary. In other cases it will be undefined by default,
# i.e. equal to the empty string (without even quotation marks).

SHELL := bash
.PHONY: show_params \
  input_subsamples \
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
  overview \
  goods_by_income_decile


##=##=##=##=##=##=##=## Variables

##=##=##=##  Non-file variables

subsample?=1
  # default value; can be overridden from the command line, as in "make raw subsample=10"
  # valid values are 1, 10, 100 and 1000
ss=$(strip $(subsample))# removes trailing space
vat_strategy?=approx
  # default value; can be overridden from command line, ala "make raw vat_strategy=detail"
  # possibilities: approx, detail, const, prop_2018_10_31
s_vat_strategy=$(strip $(vat_strategy))# removes trailing space
vat_flat_rate?=
  # by default it is the empty string, without even quotation marks
s_vat_flat_rate=$(patsubst "%",%,$(strip $(vat_flat_rate)))
  # removes trailing space and "s
strategy_suffix=$(strip $(s_vat_strategy)_$(s_vat_flat_rate))

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
households = \
  output/vat/data/recip-$(ss)/households.$(strategy_suffix).csv \
  output/vat/data/recip-$(ss)/households_decile_summary.$(strategy_suffix).csv
people_1 =           output/vat/data/recip-$(ss)/people_1.csv
people_2_buildings = output/vat/data/recip-$(ss)/people_2_buildings.csv
people_3_purchases = \
  output/vat/data/recip-$(ss)/people_3_purchases.$(strategy_suffix).csv
people_4_income_taxish = \
  output/vat/data/recip-$(ss)/people_4_income_taxish.$(strategy_suffix).csv
purchases_1 =        output/vat/data/recip-$(ss)/purchases_1.csv \
                     output/vat/data/recip-$(ss)/purchases_1_5_no_origin.csv
purchases_2_vat =    output/vat/data/recip-$(ss)/purchases_2_vat.$(strategy_suffix).csv
purchase_sums =      output/vat/data/recip-$(ss)/purchase_sums.$(strategy_suffix).csv
vat_rates = \
  output/vat/data/recip-$(ss)/vat_coicop.$(strategy_suffix).csv \
  output/vat/data/recip-$(ss)/vat_cap_c.$(strategy_suffix).csv \
  output/vat/data/recip-$(ss)/vat_coicop_brief.$(strategy_suffix).csv \
  output/vat/data/recip-$(ss)/vat_cap_c_brief.$(strategy_suffix).csv

purchase_pics = \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/frequency.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/quantity.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/value.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/vat-in-pesos,max.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/vat-in-pesos,min.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/logx/quantity.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/logx/value.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/logx/vat-in-pesos,max.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/purchases/logx/vat-in-pesos,min.png

people_pics = \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/age.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/education.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/income,by-age-decile.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/income.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/spending-per-month.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/transactions-per-month.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/logx/income,by-age-decile.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/logx/income.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/people/logx/spending-per-month.png

household_pics = \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/households/income.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/households/logx/income.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/households/max-edu.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/households/oldest.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/households/size.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/households/transactions-per-month.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/households/VAT-over-consumption,-by-income-decile.png \
  output/vat/pics/recip-$(ss)/$(strategy_suffix)/households/youngest.png

pics = $(purchase_pics) $(people_pics) $(household_pics)

overview = output/vat/tables/recip-$(ss)/overview.$(strategy_suffix).csv

goods_by_income_decile = \
  output/vat/tables/recip-$(ss)/goods_by_income_decile.csv \
  output/vat/tables/recip-$(ss)/goods,first_six_deciles.csv


##=##=##=##=##=##=##=## Recipes

show_params:
	echo "subsample: " $(subsample)
	echo "vat strategy: " $(vat_strategy)
	echo "vat flat rate: " $(vat_flat_rate)
	echo "strategy suffix: " $(strategy_suffix)

##=##=##=## subsample, or very slightly tweak, some input data sets

input_subsamples: $(input_subsamples)
$(input_subsamples): python/subsample.py $(enph_orig)
	date
	# Next: Validating command-line arguments.
	$(python_from_here) python/common/cl_args.py $(subsample) $(vat_strategy) $(vat_flat_rate)
	$(python_from_here) python/subsample.py

vat_rates: $(vat_rates)
$(vat_rates): python/build/vat_rates.py \
  python/build/output_io.py \
  data/vat/vat-by-coicop.csv \
  data/vat/vat-for-capitulo-c.csv
	date
	$(python_from_here) python/build/vat_rates.py $(subsample) $(vat_strategy) $(vat_flat_rate)


##=##=##=## Build data from the ENPH

buildings: $(buildings)
$(buildings): python/build/buildings.py \
  python/build/classes.py \
  python/build/output_io.py \
  $(input_subsamples)
	date
	$(python_from_here) python/build/buildings.py $(subsample) $(vat_strategy) $(vat_flat_rate)

people_1: $(people_1)
$(people_1): python/build/people/main.py \
  python/build/people/files.py \
  python/build/output_io.py \
  $(input_subsamples)
	date
	$(python_from_here) python/build/people/main.py $(subsample) $(vat_strategy) $(vat_flat_rate)

people_2_buildings: $(people_2_buildings)
$(people_2_buildings): python/build/people_2_buildings.py \
  python/build/output_io.py \
  $(buildings) $(people_1)
	date
	$(python_from_here) python/build/people_2_buildings.py $(subsample) $(vat_strategy) $(vat_flat_rate)

people_3_purchases: $(people_3_purchases)
$(people_3_purchases): python/build/people_3_purchases.py \
  python/build/output_io.py \
  $(people_2_buildings) $(purchase_sums)
	date
	$(python_from_here) python/build/people_3_purchases.py $(subsample) $(vat_strategy) $(vat_flat_rate)

people_4_income_taxish: $(people_4_income_taxish)
$(people_4_income_taxish): python/build/people_4_income_taxish.py \
  python/build/output_io.py \
  python/build/ss_schedules.py \
  $(people_3_purchases)
	date
	$(python_from_here) python/build/people_4_income_taxish.py $(subsample) $(vat_strategy) $(vat_flat_rate)

households: $(households)
$(households): python/build/households.py \
  python/common/util.py \
  python/build/output_io.py \
  $(people_4_income_taxish)
	date
	$(python_from_here) python/build/households.py $(subsample) $(vat_strategy) $(vat_flat_rate)

purchases_1: $(purchases_1)
$(purchases_1): python/build/purchases/main.py \
  python/build/classes.py \
  python/build/output_io.py \
  python/build/purchases/nice_purchases.py \
  python/build/purchases/medios.py \
  python/build/purchases/articulos.py \
  python/build/purchases/capitulo_c.py \
  $(input_subsamples)
	date
	$(python_from_here) python/build/purchases/main.py $(subsample) $(vat_strategy) $(vat_flat_rate)

purchases_2_vat: $(purchases_2_vat)
$(purchases_2_vat): python/build/purchases_2_vat.py \
  python/build/output_io.py \
  python/build/legends.py \
  $(vat_rates) \
  output/vat/data/recip-$(ss)/purchases_1.csv
	date
	$(python_from_here) python/build/purchases_2_vat.py $(subsample) $(vat_strategy) $(vat_flat_rate)

purchase_sums: $(purchase_sums)
$(purchase_sums): python/build/purchase_sums.py \
  python/build/output_io.py \
  $(purchases_2_vat)
	date
	$(python_from_here) python/build/purchase_sums.py $(subsample) $(vat_strategy) $(vat_flat_rate)


##=##=##=## Make charts, diagrams, tiny latex tables

purchase_pics: $(purchase_pics)
$(purchase_pics): python/report/pics/purchases.py \
  $(purchases_2_vat)
	date
	$(python_from_here) python/report/pics/purchases.py $(subsample) $(vat_strategy) $(vat_flat_rate)

household_pics: $(household_pics)
$(household_pics): python/report/pics/households.py \
  $(households)
	date
	$(python_from_here) python/report/pics/households.py $(subsample) $(vat_strategy) $(vat_flat_rate)

people_pics: $(people_pics)
$(people_pics): python/report/pics/people.py \
  $(people_4_income_taxish)
	date
	$(python_from_here) python/report/pics/people.py $(subsample) $(vat_strategy) $(vat_flat_rate)

pics: $(pics)

overview: $(overview)
$(overview): python/report/tables/overview.py \
  python/common/util.py \
  python/build/output_io.py \
  python/build/people/files.py \
  $(households)
	date
	$(python_from_here) python/report/tables/overview.py $(subsample) $(vat_strategy) $(vat_flat_rate)

# PITFALL: Always reads households from the detail vat strategy, because vat irrelevant.
goods_by_income_decile: $(goods_by_income_decile)
$(goods_by_income_decile): python/build/goods-by-income-decile.py \
  output/vat/data/recip-$(ss)/households.detail_.csv \
  output/vat/data/recip-$(ss)/purchases_1_5_no_origin.csv
	date
	$(python_from_here) python/build/goods-by-income-decile.py $(subsample) $(vat_strategy) $(vat_flat_rate)
