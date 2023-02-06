if True:
  import numpy as np
  import pandas as pd
  import os as os
  #
  import matplotlib
  import matplotlib.pyplot as plt
  import matplotlib.patches as mpatches


def bar_chart_with_changes (
    # PITFALL: Must all be the same length.
    title : str,
    xlabel : str,
    ylabel : str,
    labels : pd.Series,  # could also be a list
    levels : pd.Series,  # could also be a list
    changes : pd.Series, # could also be a list
    save_path : str,
):

  fig, ax = plt.subplots()

  ax.bar ( labels,
           levels,
           width = 0.35,
           label='before proposed change',
           color="lightgray")

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

  ax.set_xlabel ( xlabel )
  ax.set_ylabel ( ylabel )
  ax.set_title ( title )
  ax.legend()

  plt.savefig ( save_path + ".png" )
  plt.close()

def table( df, colName ):
  df = pd.DataFrame(
    df.groupby( colName )[colName]         \
      .agg('count') )                        \
    .rename( columns = {colName:"count"} ) \
    .reset_index( level = colName )
  plt.bar( df[colName], df["count"] )

def savefig( folder, name, **kwargs ):
  if not os.path.exists(folder): os.makedirs(folder)
  plt.savefig( folder + "/" + name
             , bbox_inches='tight' # ironically, this causes xlabels that might
                            # otherwise get cut off to appear in their entirety
             , **kwargs )

def to_latex( df, folder, name ):
  if not os.path.exists(folder): os.makedirs(folder)
  filename = folder + "/" + name + ".tex"
  df.to_latex( filename )
