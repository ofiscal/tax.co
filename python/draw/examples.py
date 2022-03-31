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
  import matplotlib.patches as mpatches


def arrows_on_bars ():
  labels = ['G1', 'G2', 'G3', 'G4', 'G5']
  levels = [20, 35, 30, 35, 27]
  changes = [10, 10, -10, -10, 1]
  men_std = [2, 3, 4, 1, 2]
  women_std = [3, 5, 2, 3, 3]
  width = 0.35       # the width of the bars: can also be len(x) sequence

  fig, ax = plt.subplots()

  arrow = mpatches.FancyArrowPatch (
    (0,0), # tail
    (5,5), # head
    color = "red",
    mutation_scale = 30 ) # determines arrow width, among other things
  ax.add_patch(arrow)

  ax.bar(labels, levels, width, label='Men')
  ax.set_ylabel('Scores')
  ax.set_title('Words under the graph')
  ax.legend()
  if True: # alternatives
    # plt.show()
    plt.savefig("test-arrows.png")
  plt.close()


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
