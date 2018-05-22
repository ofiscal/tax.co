# PITFALL: Due to the magic %matplotlib command, Jupyter cannot
  # execute this using the standard exec-open-read idiom.
  # Instead, just copy it into the notebook.

%matplotlib inline
  # enable the previous line if calling from Jupyter
import matplotlib
# matplotlib.use('Agg')
  # enable the previous line if calling from the (non-gui) shell
import matplotlib.pyplot as plt
