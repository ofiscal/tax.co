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
  # These lists can also be of type pandas.Series.
  labels = ['thing1', 'thing2', 'thing3', 'thing4', 'thing5']
  levels = [20, 35, 30, 35, 27]
  changes = [10, 10, -10, -10, 1]
  width = 0.35 # the width of the bars: can also be a sequence

  fig, ax = plt.subplots()

  ax.bar(labels, levels, width, label='Men', color="lightgray")

  def arrow ( bar : int ):
    """ "bar" is an index (zero-indexed) into the data vectors."""
    ax.add_patch (
      mpatches.FancyArrowPatch (
        ( bar, levels [ bar ] ),                   # tail
        ( bar, levels [ bar ] + changes [ bar ] ), # head
        color = ( "red"
                  if (changes[bar] > 0)
                  else "green" ),
        mutation_scale = 15 # determines arrow width, among other things
      ) )

  for bar in range( 0, len ( labels ) ):
    arrow ( bar )

  ax.set_ylabel('Something to measure')
  ax.set_title('Title of the graph')
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
