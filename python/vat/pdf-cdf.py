import numpy as np
import pandas as pd

%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt


the_data = pd.DataFrame([1,2,7,2,7],columns=["x"])

def draw_cdf( series ):
  data = pd.DataFrame()
  data["x"] = pd.Series( sorted(series) )
  data["count"] = 1

  dmin = data["x"].min()
  dmax = data["x"].max()
  dstep = (dmax - dmin) / 100 # this resolution is arbitrary

  nonzero_pdf = data.groupby("x").agg('sum') # only the nonzero part of the pdf
  nonzero_pdf["nonzero_pdf"] = nonzero_pdf["count"] / nonzero_pdf["count"].sum()
  nonzero_pdf = nonzero_pdf.reset_index(level="x")

  pdf_range = pd.DataFrame()
  pdf_range["x"] = np.arange( dmin - 10*dstep, dmax + 10*dstep, dstep )
    # this 10-step (5%) buffer is arbitrary

  df = pdf_range.merge( nonzero_pdf, on = "x", how = "outer" )
  df["pdf"] = np.where( df["nonzero_pdf"].isnull(), 0, df["nonzero_pdf"] ) # np.where is like if-else
  df = df[["x","pdf"]]
  df = df.sort_values("x")
  df["cdf"] = df["pdf"].cumsum()

  # plt.plot( df["x"],df["pdf"] ) # could overlay.  in discrete distributions it's 0 a.e.
  plt.plot( df["x"],df["cdf"], 'r--' )

draw_cdf( the_data["x"] )
plt.show()   # or plt.savefig("test.png")
