exec(open("python/draw/shell-load.py").read())
  # PITFALL: shell-load has to be called before anything else
  # that uses matplotlib, or it will automatically choose the wrong backend
exec(open("python/vat/report/load.py").read())
  # load some libraries and data sets specific to the VAT analysis
  # define subsample and vat_pics_dir

purchases = oio.readStage( subsample, '/2.purchases,prices,taxes')

exec(open("python/vat/report/pics,purchases.py").read())
  # draw things
