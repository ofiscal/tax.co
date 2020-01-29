# PURPOSE
#########
# These lines belong at (or at least near)
# the top of any script which one intends to use to draw
# using matplotlib outside of a graphical environment --
# i.e. from the Python repl, or from the command line,
# but not from Jupyter.

# %matplotlib inline
  # enable the previous line if calling from Jupyter
import matplotlib
matplotlib.use('Agg')
  # enable the previous line if calling from the (non-gui) shell
import matplotlib.pyplot as plt
