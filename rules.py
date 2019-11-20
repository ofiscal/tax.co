# This code serves the same purpose as a Makefile.
# Execute it by running `make.py <what to build>`
# from the command line.
# For documentation on make.py, see
# https://github.com/zwegner/make.py

# Likely commands:
# make.py "output/phony/recip-100/tests"

enph_files = [
  "Caracteristicas_generales_personas",
  "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar",
  "Gastos_diarios_personales_Urbano",
  "Gastos_diarios_Urbano_-_Capitulo_C",
  "Gastos_diarios_Urbanos",
  "Gastos_diarios_Urbanos_-_Mercados",
  "Gastos_menos_frecuentes_-_Articulos",
  "Gastos_menos_frecuentes_-_Medio_de_pago",
  "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar",
  "Gastos_personales_Rural",
  "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar",
  "Gastos_semanales_Rural_-_Capitulo_C",
  "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar",
  "Gastos_semanales_Rurales",
  "Gastos_semanales_Rurales_-_Mercados",
  "Viviendas_y_hogares" ]

enph_orig = [ "data/enph-2017/2_unzipped/csv/" + fn + ".csv"
              for fn in enph_files ]

python = "PYTHONPATH='.' python3"

strategies = ["detail"]
subsamples_i = [1,10,100,1000]
subsamples = list( map( str, subsamples_i ) )
regime_years_i = [2016,2018]
regime_years = list( map( str, regime_years_i ) )

def rules(ctx):
  # for strat in strategies:
  # for yr in regime_years:
  # for ss in subsamples:
  target = "output/phony/tests"
  ctx.add_rule(
    target,
    ["output/test/recip/build_classes.txt"],
    ["touch", target] )
  ctx.add_rule(
    "output/test/build_classes.txt",
    [ "python/build/classes.py",
      "python/build/classes_test.py" ],
    [ python, "python/build/classes_test.py",
      1, "irrelevant", "irrelevant" ] )
