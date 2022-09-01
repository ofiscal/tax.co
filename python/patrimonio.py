# TODO: This runs a multivariate log-log OLS regression.
# It needs to run a *univariate* log-log OLS regression,
# where the independent variable is total income,
# because the separate income categories are too collinear
# for their partial effects to make sense. They need to make sense,
# because they'll be used to predict the income of individuals,
# and many people have only one kind of income,
# even though none of the quantiles (which describe averages of many people)
# is like that.

from   math import log
import numpy  as np
import pandas as pd
from   statsmodels.regression.linear_model import OLS


df = pd.read_csv (
  "data/DIAN-quantiles/individuals.by-patrimonio-liquido.AG-2019.csv" )

df["dividendos"] = (
  df [[
    # TODO: Will adding some subset of these five columns
    # (the only ones with "dividendos" in their names)
    # give me total dividends income in 2019 pesos?
    "Por dividendos y participaciones año 2016 (base casilla 76)",
    "Por dividendos y participaciones año 2017 y siguientes, 1a Subcédula",
    "Por dividendos y participaciones año 2017 y siguientes, 2a. Subcédula, y otros"
    "Dividendos y participaciones 2016 y anteriores, y otros",
    "Renta líquida pasiva dividendos - ECE y/o recibidos del exterior",
  ]]
  . sum ( axis="columns" ) )


# column names
x_cols = [
  "Ingresos brutos por rentas de trabajo",
  "Ingresos por ganancias ocasionales del país y del exterior",
  # "dividendos"
    # Can't include this variable in  a log-log regression,
    # because it is often 0.
]
y_col = "Total Patrimonio líquido"


# data for regression
x = df[x_cols].copy()
y = df[y_col] .copy()
for c in x_cols:
  x[c] = x[c].apply(log)
y = y.apply(log) # y is a series, whereas x is a frame,
                 # so this looks different from the previous line.
x["one"] = 1

model   = OLS(y,x)
results = model.fit()
results.params
results.tvalues
results.summary()
