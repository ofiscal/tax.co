# PURPOSE: This runs a univariate log-log OLS regression,
# where the independent variable is total income,
# on the DIAN quantiles data.
# The coefficients from this regression will, we hope,
# be useful for imputing patrimonio to wealthy people in the ENPH.
#
# OPTION: Retain only the rich.
# This can discard quantiles with wealth below a certain threshold
# before running the regression. That's appropriate IF we're only interested
# in predicting the wealth of wealthy people.
# (The tax code currently being discussed in Congress would only apply
# to people with exceptionally high net wealth.)
# See the comment "OPTION: Retain only the rich." below.
#
# RESULT: See "sanity check" at the bottom of this program.
#
# JUSTIFICATION: Why I do not run a multivariate regression:
# The separate income categories are too collinear
# for their partial effects to make sense. They need to make sense,
# because they'll be used to predict the income of individuals,
# and many people have only one kind of income,
# even though none of the quantiles (which describe averages of many people)
# is like that.

if True:
  from   math import log, exp
  import numpy  as np
  import pandas as pd
  from   statsmodels.regression.linear_model import OLS
  #
  import python.build.output_io as oio
  import python.common.common as com


#########################
### Regress DIAN data ###
#########################

dian = pd.read_csv (
  "data/DIAN-quantiles/individuals.by-patrimonio-liquido.AG-2019.csv" )
dian = dian . rename ( # strip whitespace at edges from column names
  columns = { c : c.strip()
              for c in dian.columns } )
dian["income, DIAN-style"] = ( # total income
  dian [[ "Ingresos brutos por rentas de trabajo",
        'Ingresos por ganancias ocasionales del país y del exterior',
        'Por dividendos y participaciones año 2016 (base casilla 76)',
        'Por dividendos y participaciones año 2017 y siguientes, 1a Subcédula',
        'Por dividendos y participaciones año 2017 y siguientes, 2a. Subcédula, y otros', ]]
  . sum ( axis = "columns" ) )

# OPTION: Retain only the rich.
dian_rich = dian [ dian [ "Patrimonio Bruto" ] > 1e9 ] . copy()
min_income = dian_rich["income, DIAN-style"] . min()

def log_square_income_and_constant (
    df : pd.DataFrame
) -> pd.DataFrame:
  l = "income, DIAN-style"
  return pd.DataFrame (
    { l          : df[l] . apply(log),
      l + "^2"   : df[l] . apply(
        lambda x : log(x) ** 2),
      l + "^3"   : df[l] . apply(
        lambda x : log(x) ** 3),
      "one"      : 1 } )

model   = OLS (
  ( dian_rich ["Total Patrimonio líquido"]
    . apply(log) ),
  log_square_income_and_constant (
    dian_rich ) )

results = model.fit ()
results.params
results.tvalues
results.summary()


############################
### Predict on ENPH data ###
############################

ps = oio.readUserData (
  com.subsample,
  'people_4_post_households.' + com.strategy_year_suffix )

ps["income, DIAN-style"] = (
  ps [[ "income, ganancia ocasional, 10%-taxable",
        "income, ganancia ocasional, 20%-taxable",
        "income, dividend",
        "income, labor", ]]
  . sum ( axis = "columns" ) )

ps["wealth-hat"] = (
  results.predict (
    log_square_income_and_constant ( ps ) )
  . apply ( exp ) )
ps["wealth-hat"] = np.where (
  # If someone's income is so low that their wealth should be,
  # per the input data, less than 1e9 (mil millones) pesos,
  # then we can set their wealth to 0 because it won't be taxed.
  ps["income, DIAN-style"] < min_income,
  0, # used if true
  ps["wealth-hat"] ) # used if false


####################
### Sanity check ###
####################

xx = pd.DataFrame ( {
  "income, DIAN-style" : [ x * 10 ** y
               for (x,y) in [ (1.0, 5),
                              (5.0, 5),
                              (1.0, 6),
                              (5.0, 6),
                              (1.0, 7),
                              (5.0, 7),
                              (1.0, 8),
                              (5.0, 8),
                              (1.0, 9),
                              (5.0, 9) ] ] } )

xx["wealth-hat"] = (
  results.predict (
    log_square_income_and_constant ( xx ) )
  . apply ( lambda x: exp ( min ( 100, x ) ) ) )

xx[["income, DIAN-style","wealth-hat"]]

dian[[ "income, DIAN-style",
       "Patrimonio Bruto", ]]

ps[[ "income, DIAN-style",
     "wealth-hat", ]]
