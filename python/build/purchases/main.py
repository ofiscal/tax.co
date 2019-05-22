import sys
import numpy as np

from python.build.classes import Correction
from itertools import chain
import python.common.misc as com
import python.common.cl_args as cl
import python.build.output_io as oio

# input files
import python.build.purchases.nice_purchases as nice_purchases
import python.build.purchases.medios as medios
import python.build.purchases.articulos as articulos
import python.build.purchases.capitulo_c as capitulo_c


purchases = cl.collect_files(
  ( articulos.files
    # + medios.files
      # The tax only applies if the purchase is more than 880 million pesos,
      # and the data only records purchases of a second home.
    + capitulo_c.files
    + nice_purchases.files )
  , subsample = cl.subsample
)

for c in (
  [ Correction.Replace_Substring_In_Column(
      "quantity", ",", "." )
  , Correction.Replace_Missing_Values(
      "quantity", 1 )
  , Correction.Change_Column_Type(
      "coicop", str )
  , Correction.Replace_Entirely_If_Substring_Is_In_Column(
      "coicop", "inv", np.nan )
  ] + list( chain.from_iterable( [
    [ Correction.Change_Column_Type( colname, str )
    , Correction.Replace_In_Column(
        colname
        , { ' ' : np.nan
            # 'nan's are created from the cast to type str
            , "nan" : np.nan } ) ]
    for colname in ["where-got", "coicop", "freq", "how-got", "value"] ] ) )
  ): purchases = c.correct( purchases )

purchases = com.to_numbers(purchases)

# Include only rows with a coicop-like variable and a value.
purchases = purchases[
  # Why: For every file but "articulos", observations with no coicop have
  # no value, quantity, is-purchase or frequency. And only 63 / 211,000
  # observations in "articulos" have a missing COICOP. A way to see that
    # (which works if the file-origin variable is reenabled):
    # df0 = data.purchases[ data.purchases[ "coicop" ] . isnull() ]
    # util.dwmByGroup( "file-origin", df0 )
  ( (  ~ purchases[ "coicop"          ] . isnull())
    | (~ purchases[ "25-broad-categs" ] . isnull()) )
  & (  ~ purchases[ "value"           ] . isnull())
]

for c in [ # how-got=1 -> is-purchase=1, nan -> nan, otherwise -> 0
  Correction.Apply_Function_To_Column(
    "how-got"
    , lambda x: 1 if x==1 else
      # HACK: x >= 0 yields True for numbers, False for NaN
      (0 if x >= 0 else np.nan) )
  , Correction.Rename_Column( "how-got", "is-purchase" )
]: purchases = c.correct( purchases )

oio.saveStage(cl.subsample, purchases, 'purchases_1')
