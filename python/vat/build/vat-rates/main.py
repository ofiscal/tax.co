# WEIRD: This program creates 4 separate bridges, one for each subsample, even though they are identical.
# These data sets are tiny; it seems better to treat them like the others than to complicate the code.

import sys
import pandas as pd
import numpy as np

import python.vat.build.classes as classes
import python.vat.build.common as common
import python.vat.build.output_io as oio


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.

vat_cap_c = pd.read_csv( "data/vat/" + "vat-for-capitulo-c.csv"
                       , encoding = "latin1"
            ) . rename( columns = { "CODE" : "25-broad-categs"
                                  , "DESCRIPTION" : "description"
            } )
vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                        , sep = ";"
                        , encoding = "latin1" )

for (vat,frac) in [ ("vat"    ,     "vat frac")
                  , ("vat, min", "vat frac, min")
                  , ("vat, max", "vat frac, max") ]:
  vat_cap_c[frac]  = vat_cap_c[vat]  / (1 + vat_cap_c[vat])
  vat_coicop[frac] = vat_coicop[vat] / (1 + vat_coicop[vat])

  # Multiplying vat-fraction by value (payment)
    # results in the fraction  of the value attributable to the vat.
    # For instance, if the VAT were 20%, then (0.2 / 1.2) is that fraction.

oio.saveStage(subsample, vat_coicop, '/vat_coicop')
oio.saveStage(subsample, vat_cap_c, '/vat_cap_c')
