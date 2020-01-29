# PURPOSE
#########
# These lines belong at (or at least near)
# the top of any Jupyter notebook from which one intends to draw
# using matplotlib.

# PITFALL
#########
# Due to the magic %matplotlib command, Jupyter cannot
# execute this using the standard exec-open-read idiom.
# Instead, just copy these lines into the notebook.

%matplotlib inline
  # enable the previous line if calling from Jupyter
import matplotlib
# matplotlib.use('Agg')
  # enable the previous line if calling from the (non-gui) shell
import matplotlib.pyplot as plt
