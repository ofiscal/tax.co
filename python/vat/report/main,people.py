exec(open("python/draw/shell-load.py").read())
  # PITFALL: shell-load has to be called before anything else
  # that uses matplotlib, or it will automatically choose the wrong backend
exec(open("python/vat/report/load.py").read())
  # load some libraries and data sets specific to the VAT analysis
  # define subsample and vat_pics_dir

people = oio.readStage( subsample, '/5.person-demog-expenditures')

# TODO: Centralize this code, which is (nearly) duplicated between build_late.py and main,people.py
edu_key = { 1 : "Ninguno",
      2 : "Preescolar",
      3 : "Basica\n Primaria",
      4 : "Basica\n Secundaria",
      5 : "Media",
      6 : "Superior o\n Universitaria",
      9 : "No sabe,\n no informa" }
people["education"] = pd.Series( pd.Categorical(
    pd.Categorical( people["education"]
                   , categories = list( edu_key.values() )
                   , ordered = True) ) )

exec(open("python/vat/report/pics,people.py").read())
  # draw things
