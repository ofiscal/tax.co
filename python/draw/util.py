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

def cdf ( series,
          logx = False,
          with_mean = True,
          with_pdf = False,
          xmin = None,
          xmax = None,
          **kwargs ):
  data = pd.DataFrame()
  data["x"] = pd.Series( sorted(series) )
  data["count"] = 1

  dmin = data["x"].min()
  if xmin != None:
    dmin = max(dmin,xmin)
  dmax = data["x"].max()
  if xmax != None:
    dmax = min(dmax,xmax)
  dstep = (dmax - dmin) / 500 # this resolution is arbitrary

  pdf = data.groupby("x").agg('sum')
    # only the nonzero part of the pdf
  pdf["nonzero_pdf"] = pdf["count"] / pdf["count"].sum()
  pdf = pdf.reset_index(level="x")

  pdf_range = pd.DataFrame()
  pdf_range["x"] = np.arange( dmin - 10*dstep, dmax + 10*dstep, dstep )
    # this 10-step (5%) buffer is arbitrary

  df = pdf_range.merge( pdf, on = "x", how = "outer" )
  df["pdf"] = np.where( df["nonzero_pdf"].isnull(), 0, df["nonzero_pdf"] )
    # np.where is like if-else
  df = df[["x","pdf"]]
  df = df.sort_values("x")
  df["cdf"] = df["pdf"].cumsum()

  if logx:
    plt.xscale("log")
  if with_pdf: # for insufficiently "lumpy" variables, the pdf is zero almost everywhere
    plt.plot( df["x"],df["pdf"] )
  if with_mean:
    plt.axvline( series.mean() )
    plt.text( series.mean(), 0,
              "mean = " + format( series.mean(), '.2e') )

  plt.gca().set_xlim(left=dmin,right=dmax)
  plt.plot( df["x"],df["cdf"], **kwargs )

def single_cdf( series, xlabel, **kwargs ):
  plt.grid(color='b', linestyle=':', linewidth=0.5)
  plt.xlabel(xlabel)
  plt.ylabel("Probability")
  cdf( series, **kwargs )

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
