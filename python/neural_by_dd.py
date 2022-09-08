# PURPOSE:
# OLS appeared incapable of good predictions at the very highest quantiles.
# This uses a neural network instead.
# Thanks to Daniel Duque.
#
# OPTION: Retain only the rich.
# This can discard quantiles with wealth below a certain threshold
# before running the regression.
# It improves prediction quality on such people,
# at the cost of worthless predictions for the poor.
# That's appropriate IF we're only interested
# in predicting the wealth of wealthy people.
# (The tax code currently being discussed in Congress would only apply
# to people with exceptionally high net wealth.)
# See the comment "OPTION: Retain only the rich." below.

from   math import log, exp
import numpy  as np
from   os import path
import pandas as pd
from   sklearn import neural_network
from   sklearn.model_selection import train_test_split
import time
from   typing import Tuple, List


##########################
### Ingest, clean data ###
##########################

dian = pd.read_csv (
  path.join (
    "data/DIAN-quantiles/",
    "individuals.by-patrimonio-liquido.AG-2019.csv" ) )

dian = ( dian
         . rename ( # strip whitespace at edges from column names
           columns = { c : c.strip()
                       for c in dian.columns } )
         . rename (
           columns = { "Total Patrimonio líquido" : "wealth" } ) )

# OPTION: Retain only the rich.
dian_rich = dian[ dian["wealth"] > 5e8 ] . copy()

dian_rich["income, DIAN-style"] = (
  # I don't use the simpler label "income" because that would clobber
  # another column that already exists in the DANE-based data.
  dian_rich [[
    "Ingresos brutos por rentas de trabajo",
    'Ingresos por ganancias ocasionales del país y del exterior',
    'Por dividendos y participaciones año 2016 (base casilla 76)',
    'Por dividendos y participaciones año 2017 y siguientes, 1a Subcédula',
    'Por dividendos y participaciones año 2017 y siguientes, 2a. Subcédula, y otros', ]]
  . sum ( axis = "columns" ) )

for c in ["income, DIAN-style", "wealth"]:
  dian_rich["log " + c] = dian_rich[c] . apply(log)


##################################
### Determining what NN to use ###
##################################

def go ( layers : Tuple[int]
       )       -> pd.Series:

  np.random.seed(seed=int(time.time()))

  ################
  ### NN magic ###
  ################

  X_train, X_test, y_train, y_test = train_test_split (
    dian_rich [[ "log income, DIAN-style" ]],
    dian_rich ["log wealth"],
    test_size = 0.2,
    random_state = 0 )

  # Model the data in a neural network.
  patrmod = neural_network.MLPRegressor (
    hidden_layer_sizes = layers,
    solver             = "lbfgs",
    max_iter           = 1000 )
  patrmod.fit ( X_train, y_train )

  ###############
  ### Predict ###
  ###############

  nn_train = pd.DataFrame (
    { "log income, DIAN-style" : X_train["log income, DIAN-style"],
      "log wealth"             : y_train,
      "log wealth^"            : pd.Series (
        patrmod.predict ( X_train ),
        index = X_train.index ),
      "test data" : 0 # This would more naturally be a bool, but if it is,
                      # then pandas omits it when running describe().
     } )

  nn_test = pd.DataFrame (
    { "log income, DIAN-style" : X_test["log income, DIAN-style"],
      "log wealth"             : y_test,
      "log wealth^"            : pd.Series (
        patrmod.predict ( X_test ),
        index = X_test.index ),
      "test data"          : 1 } )

  nn = ( pd.concat ( [nn_train, nn_test],
                     axis = "rows" )
         . sort_values ( "log income, DIAN-style" ) )

  MSE = ( ( ( nn["log wealth"]
              - nn["log wealth^"] )
            ** 2 )
          . sum ()
          / len(nn) )

  return {
    "splits" : (X_train, X_test, y_train, y_test),
    "model" : patrmod,
    "data" : nn,
    "layers" : str(layers),
    "MSE" : MSE }

def try_some_NN_shapes_factory():

  MSEs = pd.DataFrame (
    columns = ["n runs",
               "mean MSE over runs"] )

  def try_some_NN_shapes (
      layers_list : List [ Tuple [ int ] ] ):
    # This is IO -- it just modifies MSEs.
    # It can be run more than once, with the same arguments,
    # to get different estimates (since they're random)
    # and improve the data in MSEs.

    nonlocal MSEs

    for layers in layers_list:
      sl = str(layers)
      mse = go (layers) ["MSE"]
      if not sl in MSEs.index:
        MSEs = MSEs.append (
          pd.Series ( { "n runs"               : 1,
                          "mean MSE over runs" : mse },
                        name = sl ) )
      else:
        oldRuns    = MSEs.loc[ sl, "n runs"]
        oldMeanMSE = MSEs.loc[ sl, "mean MSE over runs"]
        newRuns    = oldRuns + 1
        newMeanMSE = (oldRuns * oldMeanMSE + mse) / newRuns
        print ( sl, mse )
        print ( oldRuns, oldMeanMSE, newRuns, newMeanMSE )
        MSEs.loc[ sl, "n runs"]             = newRuns
        MSEs.loc[ sl, "mean MSE over runs"] = newMeanMSE

  return ( try_some_NN_shapes,
           lambda: MSEs )

(t,show) = try_some_NN_shapes_factory()

for i in range(10):
  t ( [ (x,y)
        for x in range(8,27)
        for y in range(2,x)
        if x%2 == y%2 == 0 ]
      +
      [ (x,y,z)
        for x in range(8,27)
        for y in range(6,x)
        for z in range(4,y)
        if x%2 == y%2 == z%2 == 0 ] )

pd.options.display.min_rows = 100
show().sort_values("mean MSE over runs")


# Keeping all the data, I get these as the best layouts:
#
# shape           runs            MSE averaged over those runs
# (26, 16, 6)     19.0            1.776743
# (26, 22, 20)    30.0            1.781108
# (16, 14, 12)    62.0            1.787907
# (26, 20, 18)    30.0            1.789586
# (24, 18, 14)    31.0            1.790914
# (24, 14)        32.0            1.792104
# (24, 18, 16)    31.0            1.792264
# (24, 18, 6)     19.0            1.794339
# (22, 14, 12)    32.0            1.794344
# (22, 20, 8)     19.0            1.794474
# (26, 20, 8)     19.0            1.794503
# (26, 10, 8)     19.0            1.795395
# (24, 16, 14)    31.0            1.795790
# (20, 14, 12)    34.0            1.796458
# (26, 20, 10)    19.0            1.796811
# (26, 22, 10)    19.0            1.797499
# (26, 20, 14)    30.0            1.798367
# (26, 22, 14)    30.0            1.798610
# (20, 16, 8)     21.0            1.799083
# (24, 22, 20)    31.0            1.799248
# (24, 18, 12)    31.0            1.799935
# (26, 14)        31.0            1.800362
# (22, 14, 10)    20.0            1.801524
# (18, 16)        63.0            1.802058
