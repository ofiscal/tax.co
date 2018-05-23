import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt


def cdf( series, logx = False, with_mean = True, with_pdf = False, **kwargs ):
  data = pd.DataFrame()
  data["x"] = pd.Series( sorted(series) )
  data["count"] = 1

  dmin = data["x"].min()
  dmax = data["x"].max()
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
  plt.plot( df["x"],df["cdf"], **kwargs )


def single_cdf( series, xlabel, saveto, **kwargs ):
  plt.grid(color='b', linestyle=':', linewidth=0.5)
  plt.xlabel(xlabel)
  plt.ylabel("Probability")
  cdf( series, **kwargs )
  plt.savefig( saveto )
