# PURPOSE: This runs a univariate log-log OLS regression,
# where the independent variable is total income,
# on the DIAN quantiles data.
# The coefficients from this regression will, we hope,
# be useful for imputing patrimonio in the ENPH.
#
# RESULT: See "sanity check" at the bottom of this program.
#
# EXPLANATION: Why not run a multivariate regression:
# The separate income categories are too collinear
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
df = df . rename ( # strip whitespace at edges from column names
  columns = { c : c.strip()
              for c in df.columns } )
df["income"] = ( # total income
  df [[ "Ingresos brutos por rentas de trabajo",
        'Ingresos por ganancias ocasionales del país y del exterior',
        'Por dividendos y participaciones año 2016 (base casilla 76)',
        'Por dividendos y participaciones año 2017 y siguientes, 1a Subcédula',
        'Por dividendos y participaciones año 2017 y siguientes, 2a. Subcédula, y otros', ]]
  . sum ( axis = "columns" ) )

x = pd.DataFrame (
  { "income" : df["income"] . apply(log),
    "one"    : 1 } )
y = df["Total Patrimonio líquido"] . apply(log)

model   = OLS(y,x)
results = model.fit()
results.params
results.tvalues
results.summary()

# Sanity check: looks insane at the extremes.
for annual_income in [ 1e6, 1e7, 1e8, 1e9 ]:
  print ( "{:e}" . format ( annual_income ) )
  print ( "{:e}" . format (
    exp ( log ( annual_income )
          * results . params [ "income" ]
          + results . params [ "one" ] ) ) )
  print()
# Results:
#
# If you make a million COP in a year,
# your savings is basically nothing. Reasonable.
# 1.000000e+06
# 5.904753e+03
#
# If you make 10 million COP in a year,
# your savings is a couple million a yaer. Reasonable.
# 1.000000e+07
# 1.905299e+06
#
# If you make 100 million COP in a year,
# your savings is about six times that. Plausible.
# 1.000000e+08
# 6.147868e+08
#
# But if you make 1000 million COP in a year,
# your savings is 200 times that? No way.
# 1.000000e+09
# 1.983746e+11
