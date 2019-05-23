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
  goods_by_income_decile \
  tests


##=##=##=##=##=##=##=## Variables

##=##=##=##  Non-file variables

subsample?=1
  # default value; can be overridden from the command line,
  # as in "make raw subsample=10"
  # possibilities: 1, 10, 100 and 1000
ss=$(strip $(subsample))
  # removes trailing space
strategy?=detail
s_strategy=$(strip $(strategy))
strategy_suffix=$(strip $(s_strategy))
regime_year?=2016
  # possibilities: 2016, 2018
yr=$(strip $(regime_year))
strategy_year_suffix=$(strategy_suffix).$(yr)

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
  output/vat/data/recip-$(ss)/households.$(strategy_year_suffix).csv \
  output/vat/data/recip-$(ss)/households_decile_summary.$(strategy_year_suffix).csv
people_1 =           output/vat/data/recip-$(ss)/people_1.csv
people_2_buildings = output/vat/data/recip-$(ss)/people_2_buildings.csv
people_3_purchases = \
  output/vat/data/recip-$(ss)/people_3_purchases.$(strategy_suffix).csv
people_4_income_taxish = \
  output/vat/data/recip-$(ss)/people_4_income_taxish.$(strategy_year_suffix).csv
purchases_1 =        output/vat/data/recip-$(ss)/purchases_1.csv
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

overview = \
  output/vat/tables/recip-$(ss)/overview.$(strategy_year_suffix).csv

goods_by_income_decile = \
  output/vat/tables/recip-$(ss)/goods_by_income_decile.csv \
  output/vat/tables/recip-$(ss)/goods,first_six_deciles.csv


##=##=##=##=##=##=##=## Recipes

##=##=##=## testing

##=## minor tests

lag:
	bash bash/overview_lag.sh $(ss) $(strategy) $(yr)

diff:
	$(python_from_here) python/test/overview_diff.py \
          $(subsample) $(strategy) $(yr)

show_params:
	echo "subsample: " -$(subsample)-
	echo "tax regime year: " -$(yr)-
	echo "vat strategy: " -$(strategy)-
	echo "strategy suffix: " -$(strategy_suffix)-
	echo "strategy_year_suffix: " -$(strategy_year_suffix)


##=## the run-after-every-change test suite

# Sufficiently simple and fast tests can stay in the master "tests" recipe here.
# But for any test complex enough to require an output file,
# make that output file a dependency.
tests: output/test/purchase_input_formats.txt
	date
	$(python_from_here) python/build/classes_tests.py \
          $(subsample) $(strategy) $(yr)
#	$(python_from_here) python/build/purchases/main_test.py \
#          $(subsample) $(strategy) $(yr)
#	$(python_from_here) python/common/misc_test.py \
#          $(subsample) $(strategy) $(yr)
	printf '\nAll tests passed.\n\n'

output/test/purchase_input_formats.txt: \
  python/build/classes.py \
  python/build/output_io.py \
  python/build/purchases/input_formats.py \
  python/build/purchases/nice_purchases.py \
  python/build/purchases/articulos.py \
  python/build/purchases/capitulo_c.py \
  python/common/misc.py
	date
	$(python_from_here) python/build/purchases/input_formats.py \
          1 detail 2016 # Aside from subsample, these arguments are unused.
                        # (They are still needed, or cl_args.py will err.)
                        # Sample size is hardcoded to 1 because otherwise
                        # certain kinds of rare values are never encountered.


##=##=##=## subsample, or very slightly tweak, some input data sets

input_subsamples: $(input_subsamples)
$(input_subsamples): python/subsample.py $(enph_orig)
	date
	# Next: Validating command-line arguments.
	$(python_from_here) python/common/cl_args.py $(subsample) $(strategy) $(yr)
	$(python_from_here) python/subsample.py

vat_rates: $(vat_rates)
$(vat_rates): python/build/vat_rates.py \
  python/build/output_io.py \
  data/vat/vat-by-coicop.csv \
  python/common/misc.py \
  python/build/classes.py \
  data/vat/vat-for-capitulo-c.csv
	date
	$(python_from_here) python/build/vat_rates.py $(subsample) $(strategy) $(yr)


##=##=##=## Build data from the ENPH

buildings: $(buildings)
$(buildings): python/build/buildings.py \
  python/build/classes.py \
  python/build/output_io.py \
  python/common/misc.py \
  $(input_subsamples)
	date
	$(python_from_here) python/build/buildings.py $(subsample) $(strategy) $(yr)

people_1: $(people_1)
$(people_1): python/build/people/main.py \
  python/build/people/files.py \
  python/build/output_io.py \
  python/common/misc.py \
  python/build/classes.py \
  $(input_subsamples)
	date
	$(python_from_here) python/build/people/main.py $(subsample) $(strategy) $(yr)

people_2_buildings: $(people_2_buildings)
$(people_2_buildings): python/build/people_2_buildings.py \
  python/build/output_io.py \
  python/common/misc.py \
  python/build/classes.py \
  $(buildings) $(people_1)
	date
	$(python_from_here) python/build/people_2_buildings.py $(subsample) $(strategy) $(yr)

people_3_purchases: $(people_3_purchases)
$(people_3_purchases): python/build/people_3_purchases.py \
  python/build/output_io.py \
  python/common/misc.py \
  python/build/classes.py \
  $(people_2_buildings) $(purchase_sums)
	date
	$(python_from_here) python/build/people_3_purchases.py $(subsample) $(strategy) $(yr)

people_4_income_taxish: $(people_4_income_taxish)
$(people_4_income_taxish): python/build/people_4_income_taxish.py \
  python/build/output_io.py \
  python/build/ss_schedules.py \
  python/regime/r$(yr).py \
  python/common/misc.py \
  python/build/classes.py \
  $(people_3_purchases)
	date
	$(python_from_here) python/build/people_4_income_taxish.py $(subsample) $(strategy) $(yr)

households: $(households)
$(households): python/build/households.py \
  python/common/util.py \
  python/build/output_io.py \
  python/regime/r$(yr).py \
  $(people_4_income_taxish)
	date
	$(python_from_here) python/build/households.py $(subsample) $(strategy) $(yr)

purchases_1: $(purchases_1)
$(purchases_1): python/build/purchases/main.py \
  python/build/classes.py \
  python/build/output_io.py \
  python/build/purchases/nice_purchases.py \
  python/build/purchases/articulos.py \
  python/build/purchases/capitulo_c.py \
  python/common/misc.py \
  python/build/classes.py \
  $(input_subsamples)
	date
	$(python_from_here) python/build/purchases/main.py $(subsample) $(strategy) $(yr)

purchases_2_vat: $(purchases_2_vat)
$(purchases_2_vat): python/build/purchases_2_vat.py \
  python/build/output_io.py \
  python/build/legends.py \
  $(vat_rates) \
  python/common/misc.py \
  python/build/classes.py \
  output/vat/data/recip-$(ss)/purchases_1.csv
	date
	$(python_from_here) python/build/purchases_2_vat.py $(subsample) $(strategy) $(yr)

purchase_sums: $(purchase_sums)
$(purchase_sums): python/build/purchase_sums.py \
  python/build/output_io.py \
  python/common/misc.py \
  python/build/classes.py \
  $(purchases_2_vat)
	date
	$(python_from_here) python/build/purchase_sums.py $(subsample) $(strategy) $(yr)


##=##=##=## Make charts, diagrams, tiny latex tables

purchase_pics: $(purchase_pics)
$(purchase_pics): python/report/pics/purchases.py \
  python/draw/util.py \
  python/common/misc.py \
  python/common/cl_args.py \
  $(purchases_2_vat)
	date
	$(python_from_here) python/report/pics/purchases.py $(subsample) $(strategy) $(yr)

household_pics: $(household_pics)
$(household_pics): python/report/pics/households.py \
  python/draw/util.py \
  python/common/misc.py \
  python/common/cl_args.py \
  $(households)
	date
	$(python_from_here) python/report/pics/households.py $(subsample) $(strategy) $(yr)

people_pics: $(people_pics)
$(people_pics): python/report/pics/people.py \
  python/draw/util.py \
  python/common/misc.py \
  python/common/cl_args.py \
  $(people_4_income_taxish)
	date
	$(python_from_here) python/report/pics/people.py $(subsample) $(strategy) $(yr)

pics: $(pics)

overview: $(overview)
$(overview): python/report/overview.py \
  python/common/util.py \
  python/build/output_io.py \
  python/build/people/files.py \
  python/regime/r$(yr).py \
  python/draw/util.py \
  python/common/misc.py \
  python/common/cl_args.py \
  python/build/classes.py \
  $(households)
	date
	$(python_from_here) python/report/overview.py $(subsample) $(strategy) $(yr)

# PITFALL: Always reads households from the detail vat strategy, because vat irrelevant.
goods_by_income_decile: $(goods_by_income_decile)
$(goods_by_income_decile): python/build/goods-by-income-decile.py \
  output/vat/data/recip-$(ss)/households.detail_.csv \
  output/vat/data/recip-$(ss)/purchases_1.csv
	date
	$(python_from_here) python/build/goods-by-income-decile.py $(subsample) $(strategy) $(yr)
