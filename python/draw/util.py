import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt


def cdf( series, **kwargs ):
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

  # plt.plot( df["x"],df["pdf"] )
    # could overlay, but in discrete distributions, is zero almost everywhere
  plt.plot( df["x"],df["cdf"], **kwargs )
