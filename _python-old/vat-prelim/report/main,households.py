exec(open("python/draw/shell-load.py").read())
  # PITFALL: shell-load has to be called before anything else
  # that uses matplotlib, or it will automatically choose the wrong backend
exec(open("python/vat/report/load.py").read())
  # load some libraries and data sets specific to the VAT analysis
  # define subsample and vat_pics_dir

households =                  \
    oio.readStage( subsample, '/6.households' )
households_decile_summary =   \
    oio.readStage( subsample, '/9.households_decile_summary')

exec(open("python/vat/report/pics,households.py").read())
  # draw things
