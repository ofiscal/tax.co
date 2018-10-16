import sys
import numpy as np

from python.vat.build.classes import Correction
import python.vat.build.common as common
import python.vat.build.output_io as oio

# input files
import python.vat.build.purchases.nice_purchases as nice_purchases
import python.vat.build.purchases.medios as medios
import python.vat.build.purchases.articulos as articulos
import python.vat.build.purchases.capitulo_c as capitulo_c


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.

purchases = common.collect_files(
  articulos.files
  # + medios.files
    # The tax only applies if the purchase is more than 880 million pesos,
    # and the data only records purchases of a second home.
  + capitulo_c.files
  + nice_purchases.files
  , subsample = subsample
)

for c in [ # TODO ? This might be easier to understand without the Correction class.
  Correction.Replace_Substring_In_Column( "quantity", ",", "." )
  , Correction.Replace_Missing_Values( "quantity", 1 )

  , Correction.Change_Column_Type( "coicop", str )
  , Correction.Replace_Entirely_If_Substring_Is_In_Column( "coicop", "inv", np.nan )

  # The rest of these variables need the same number-string-cleaning process:
    , Correction.Change_Column_Type( "where-got", str )
      # same as this: purchases["where-got"] = purchases["where-got"] . astype( str )
    , Correction.Replace_In_Column( "where-got"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } ) # 'nan's are created from the cast to type str
      # same as this: purchases["where-got"] = purchases["where-got"] . replace( <that same dictionary> )

    , Correction.Change_Column_Type( "coicop", str )
    , Correction.Replace_In_Column( "coicop"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } )

    , Correction.Change_Column_Type( "freq", str )
    , Correction.Replace_In_Column( "freq"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } )

    , Correction.Change_Column_Type( "how-got", str )
    , Correction.Replace_In_Column( "how-got"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } )

    , Correction.Change_Column_Type( "value", str )
    , Correction.Replace_In_Column( "value"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } )
]: purchases = c.correct( purchases )

purchases = common.to_numbers(purchases)

purchases = purchases[ # must have a value and a coicop-like variable
  # Why: For every file but "articulos", observations with no coicop have
  # no value, quantity, is-purchase or frequency. And only 63 / 211,000
  # observations in "articulos" have a missing COICOP. A way to see that:
    # df0 = data.purchases[ data.purchases[ "coicop" ] . isnull() ]
    # util.dwmByGroup( "file-origin", df0 )
  ( (  ~ purchases[ "coicop"          ] . isnull())
    | (~ purchases[ "25-broad-categs" ] . isnull()) )
  & (  ~ purchases[ "value"           ] . isnull())
]

for c in [ # how-got 1 -> is-purchase 1, nan -> nan, otherwise -> 0
  Correction.Apply_Function_To_Column(
    "how-got"
    , lambda x: 1 if x==1 else
      # HACK: x >= 0 yields true for numbers, false for NaN
      (0 if x >= 0 else np.nan) )
  , Correction.Rename_Column( "how-got", "is-purchase" )
]: purchases = c.correct( purchases )

oio.saveStage(subsample, purchases, 'purchases_1')
