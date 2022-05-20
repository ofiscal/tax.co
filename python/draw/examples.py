# Illustrates four ways to draw figures:
# interactively and to disk,
# from Jupyter and from the shell.

if True:
  import python.draw.util as draw
  import pandas as pd
  # %matplotlib inline
    # enable the previous line if calling from Jupyter
  import matplotlib
  matplotlib.use('Agg')
    # enable the previous line if calling from the (non-gui) shell
  import matplotlib.pyplot as plt


def a_bar_chart ():
  plt.bar ( x = [1,2,3],
            height = pd.Series( [1,2,3] ) )
  plt.title("The data [1,2,3]")
  plt.xlabel("x")
  plt.ylabel("y")
  if True: # alternatives
    # plt.show()
    plt.savefig("test-bars.png")
  plt.close()

def a_cdf ():
  data = [1,2,7,2,7]
  df = pd.DataFrame( data, columns=["x"])
  draw.cdf( df["x"] )
  plt.title("The empirical CDF of the observed series " + str(data) )
  plt.xlabel("Outcome")
  plt.ylabel("Probability")
  if True: # alternatives
    # plt.show()
    plt.savefig("test-cdf.png")
  plt.close()
