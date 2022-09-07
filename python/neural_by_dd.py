# OLS appeared incapable of good predictions at the very highest quantiles.
# This uses a neural network instead.
# Thanks to Daniel Duque.

from   math import log, exp
import numpy  as np
from   os import path
import pandas as pd
from   sklearn import neural_network
from   sklearn.model_selection import train_test_split


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

dian["income, DIAN-style"] = (
  # I don't use the simpler label "income" because that would clobber
  # another column that already exists in the DANE-based data.
  dian [[ "Ingresos brutos por rentas de trabajo",
          'Ingresos por ganancias ocasionales del país y del exterior',
          'Por dividendos y participaciones año 2016 (base casilla 76)',
          'Por dividendos y participaciones año 2017 y siguientes, 1a Subcédula',
          'Por dividendos y participaciones año 2017 y siguientes, 2a. Subcédula, y otros', ]]
  . sum ( axis = "columns" ) )


################
### NN magic ###
################

X_train, X_test, y_train, y_test = train_test_split (
  dian [[ "income, DIAN-style" ]],
  dian ["wealth"],
  test_size = 0.2,
  random_state = 0 )

# Model the data in a neural network.
patrmod = neural_network.MLPRegressor (
  hidden_layer_sizes = (14,12,10,8),
  solver             = "lbfgs",
  max_iter           = 1000 )
patrmod.fit ( X_train, y_train )


###############
### Predict ###
###############

nn_train = pd.DataFrame (
  { "income, DIAN-style" : X_train["income, DIAN-style"],
    "wealth"             : y_train,
    "wealth^"            : pd.Series (
      patrmod.predict ( X_train ),
      index = X_train.index ),
    "test data" : 0 # This would more naturally be a bool, but if it is,
                    # then pandas omits it when running describe().
   } )

nn_test = pd.DataFrame (
  { "income, DIAN-style" : X_test["income, DIAN-style"],
    "wealth"             : y_test,
    "wealth^"            : pd.Series (
      patrmod.predict ( X_test ),
      index = X_test.index ),
    "test data"          : 1 } )

nn = ( pd.concat ( [nn_train, nn_test],
                   axis = "rows" )
       . sort_values ( "income, DIAN-style" ) )
