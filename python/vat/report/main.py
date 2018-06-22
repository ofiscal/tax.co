# This is designed to be called from the shell, not Jupyter.
  # Hence the first line, shell-load.py.
# It will, however, work from Jupyter, after complaining.

exec(open("python/draw/shell-load.py").read())
  # PITFALL: shell-load has to be called before anything else
  # that uses matplotlib, or it will automatically choose the wrong backend
exec(open("python/vat/report/load.py").read())
  # load some libraries and data sets specific to the VAT analysis
  # (and build those data sets out a bit)
exec(open("python/vat/report/pics.py").read())
  # draw things
