import numpy as np
import pandas as pd

# %matplotlib inline
  # enable the previous line if calling from Jupyter
import matplotlib
matplotlib.use('Agg')
  # enable the previous line if calling from the (non-gui) shell
import matplotlib.pyplot as plt


def cdf( series ):
  data = pd.DataFrame()
  data["x"] = pd.Series( sorted(series) )
  data["count"] = 1

  dmin = data["x"].min()
  dmax = data["x"].max()
  dstep = (dmax - dmin) / 100 # this resolution is arbitrary

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

  # plt.plot( df["x"],df["pdf"] )
    # could overlay, but in discrete distributions, is zero almost everywhere
  plt.plot( df["x"],df["cdf"], 'r--' )
