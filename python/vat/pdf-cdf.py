import numpy as np
import pandas as pd

%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt


## Some toy data

data = pd.DataFrame([1,2,2,7,7],columns=["x"])
data["count"] = 1
nonzero_pdf = data.groupby("x").agg('sum')
nonzero_pdf["nonzero_pdf"] = nonzero_pdf["count"] / nonzero_pdf["count"].sum()
nonzero_pdf = nonzero_pdf.reset_index(level="x")

pdf_range = pd.DataFrame()
pdf_range["x"] = np.arange(0,10,0.01) # critical : the last number here must be small

df = pdf_range.merge( nonzero_pdf, on = "x", how = "outer" )
df["pdf"] = np.where( df["nonzero_pdf"].isnull(), 0, df["nonzero_pdf"] )
df = df[["x","pdf"]]
df["cdf"] = df["pdf"].cumsum()


## draw it

plt.hist( df["x"],df["pdf"] )
plt.plot( df["x"],df["cdf"], 'r--' )
plt.show()
plt.savefig("test.png")
