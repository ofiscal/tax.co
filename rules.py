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

python = "python-from-here"

strategies = ["detail"]
subsamples_i = [1,10,100,1000]
subsamples = list( map( str, subsamples_i ) )
regime_years_i = [2016,2018]
regime_years = list( map( str, regime_years_i ) )

def rules(ctx):
  rules_for_tests(ctx)
  rules_for_data(ctx)

  target = "output/phony/all"
  ctx.add_rule(
    target,
    [ "output/phony/tests",
      "output/phony/data" ],
    [ "touch", target ] )

def rules_for_tests(ctx):
  """ tests that do not vary across subsample, strategy or year """

  tests = []
  for (ss, strat, yr) in [("1","detail","2018")]:

    target = "output/test/recip-1/build_classes.txt"
    tests.append( target )
    ctx.add_rule(
      target,
      [ "python/build/classes.py",
        "python/build/classes_test.py" ],
      [ python, "python/build/classes_test.py",
        ss, strat, yr ] )

    target = "output/test/recip-1/common_misc.txt"
    tests.append( target )
    ctx.add_rule(
      target,
      [ "python/build/output_io.py",
        "python/common/common.py",
        "python/common/misc.py",
        "python/common/misc_test.py" ],
      [ python, "python/common/misc_test.py",
        ss, strat, yr ] )

    target = "output/test/recip-1/common_util.txt"
    tests.append( target )
    ctx.add_rule(
      target,
      [ "python/build/output_io.py",
        "python/common/util.py",
        "python/common/util_test.py" ],
      [ python, "python/common/util_test.py",
        ss, strat, yr ] )

  target = "output/phony/tests"
  ctx.add_rule(
    target,
    tests,
    ["touch", target] )

def rules_for_data(ctx):
  data = []
  data = data + rules_for_subsmaple(ctx)

  target = "output/phony/data"
  ctx.add_rule(
    target,
    data,
    ["touch", target] )

def rules_for_subsmaple(ctx):
  # TODO (blocked): I asked about making this recipe more natural here:
  # https://github.com/zwegner/make.py/issues/5

  if False: # more natural, but slow
    targets = [ "data/enph-2017/recip-" + ss + "/" + e + ".csv"
                for ss in subsamples
                for e in enph_files ]
    ctx.add_rule(
      targets,
      [ "data/enph-2017/2_unzipped/csv/" + e + ".csv"
        for e in enph_files ]
      + [ "python/subsample.py",
          "python/build/datafiles.py" ],
      [ python, "python/subsample.py" ] )
    return targets

  if True: # PITFALL: fast, but unnatural, and dangerous:
           # If one of small_targets is deleted,
           # make.py won't know to rebuild it,
           # unless I delete big_target.
    subsampled_files = []

    # This builds all of the small targets
    big_target = "output/phony/subsamples"
    ctx.add_rule(
      big_target,
      [ "data/enph-2017/2_unzipped/csv/" + e + ".csv"
        for e in enph_files ] +
        [ "python/subsample.py",
          "python/build/datafiles.py" ],
      [ [ python, "python/subsample.py" ],
        [ "touch", big_target ] ] )

    for ss in subsamples:
      for e in enph_files:
        small_target = "data/enph-2017/recip-" + ss + "/" + e + ".csv"
        ctx.add_rule(
          small_target,
          [ big_target ],
          [ "touch", small_target ] ) # without this, `target` would
                     # look out of date relative to its dependencies
        subsampled_files.append( small_target )

    return [big_target] + subsampled_files
