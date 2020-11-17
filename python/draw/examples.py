# Illustrates four ways to draw figures:
# interactively and to disk,
# from Jupyter and from the shell.

import python.draw.util as draw
import pandas as pd

# %matplotlib inline
  # enable the previous line if calling from Jupyter
import matplotlib
matplotlib.use('Agg')
  # enable the previous line if calling from the (non-gui) shell
import matplotlib.pyplot as plt

data = [1,2,7,2,7]
df = pd.DataFrame( data, columns=["x"])
draw.cdf( df["x"] )
plt.title("The empirical CDF of the observed series " + str(data) )
plt.xlabel("Outcome")
plt.ylabel("Probability")
if True: # alternatives
  # plt.show()
  plt.savefig("test.png")

plt.close()
