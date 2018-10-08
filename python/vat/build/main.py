import pandas as pd
import numpy as np

import python.vat.build.common as common

# input files
import python.vat.build.buildings.files as bldg
from python.vat.build.people.main import people
from   python.vat.build.purchases.main import purchases
import python.vat.build.purchases.main as purchases_main


if True: # buildings
  buildings = common.collect_files( bldg.files )
  buildings["estrato"] = buildings["estrato"].replace(' ', np.nan)
  buildings = buildings.drop( columns = ["file-origin"] )


if True: # VAT dictionaries
  vat_cap_c = pd.read_csv( "data/vat/" + "vat-for-capitulo-c.csv"
                         , encoding = "latin1"
              ) . rename( columns = { "CODE" : "25-broad-categs"
                                    , "DESCRIPTION" : "description"
              } )
  vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                          , sep = ";"
                          , encoding = "latin1" )

  for (vat,frac) in [ ("vat"    ,     "vat frac")
                    , ("min vat", "min vat frac")
                    , ("max vat", "max vat frac") ]:
    vat_cap_c[frac]  = vat_cap_c[vat]  / (1 + vat_cap_c[vat])
    vat_coicop[frac] = vat_coicop[vat] / (1 + vat_coicop[vat])

  # Multiplying vat-fraction by value (payment)
    # results in the fraction  of the value attributable to the vat.
    # For instance, if the VAT were 20%, then (0.2 / 1.2) is that fraction.

if True: # add VAT to purchases
  purchases = purchases.merge( vat_coicop, how = "left", on="coicop" )
  purchases = purchases.merge( vat_cap_c, how = "left", on="25-broad-categs" )

  # Since vat_cap_c and vat_coicop have like-named columns, the second merge causes
  # a proliferation of like-named columns ending in _x or _y. The next section picks,
  # for each pair name_x and name_y, a master value for the name column, then discards
  # the two that were selected from.

  for (result, x, y) in [ ("vat", "vat_x","vat_y")
                      , ("min vat frac", "min vat frac_x","min vat frac_y")
                      , ("min vat frac", "max vat frac_x","max vat frac_y")
                      , ("min vat", "min vat_x","min vat_y")
                      , ("min vat", "max vat_x","max vat_y") ]:
    purchases.loc[ ~purchases[x].isnull(), result] = purchases[x]
    purchases.loc[  purchases[x].isnull(), result] = purchases[y]
    purchases = purchases.drop( columns = [x,y] )


#  purchases["freq-code"] = purchases["freq"]
#    # kept for the sake of drawing a table of purchase frequency
#    # with frequencies spread evenly across the x-axis
#  purchases["freq"].replace( purchases_main.freq_key
#                           , inplace=True )
#  purchases = purchases.drop(
#    purchases[ purchases["freq"].isnull() ]
#    .index
#  )
#
#  purchases["value"] = purchases["freq"] * purchases["value"]
#  purchases["vat-paid"] = purchases["value"] * purchases["vat-fraction"]
