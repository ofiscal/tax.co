exec(open("python/draw/shell-load.py").read())
  # PITFALL: shell-load has to be called before anything else
  # that uses matplotlib, or it will automatically choose the wrong backend
exec(open("python/vat/report/load.py").read())
  # load some libraries and data sets specific to the VAT analysis
  # define subsample and vat_pics_dir

people = oio.readStage( subsample, '/5.person-demog-expenditures')

exec(open("python/vat/report/pics,people.py").read())
  # draw things
