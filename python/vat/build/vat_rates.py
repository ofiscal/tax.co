import sys
import pandas as pd

import python.vat.build.output_io as oio


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.
  # Except for the save at the end, this argument is ignored; the program uses
  # the full sample always, because it's a small file, and merged with others.
  # If it was subsampled at 1/n, and the other one was as well,
  # then their merge would be subsampled at 1/n^2.

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

oio.saveStage(subsample, vat_coicop, 'vat_coicop')
oio.saveStage(subsample, vat_cap_c, 'vat_cap_c')

vat_coicop = vat_coicop.drop( columns = ["description","Notes"] )
vat_cap_c = vat_cap_c.drop( columns = ["description"] )

oio.saveStage(subsample, vat_coicop, 'vat_coicop_brief')
oio.saveStage(subsample, vat_cap_c, 'vat_cap_c_brief')
