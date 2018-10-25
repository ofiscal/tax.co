import sys
import pandas as pd

import python.vat.build.output_io as oio


# PITFALL|WART: If the vat_strategy is "approx" or "detail", this produces the same files,
# but saves them with different names. That's done so I can avoid using conditional logic
# in the Makefile.

subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.
  # Except for the save at the end, this argument is ignored; the program uses
  # the full sample always, because it's a small file, and merged with others.
  # If it was subsampled at 1/n, and the other one was as well,
  # then their merge would be subsampled at 1/n^2.

vat_strategy = sys.argv[2] # Valid: const | approx | detail
if vat_strategy == "const": vat_const_rate = float(sys.argv[3])  # float: 0.19, 0.107, etc;
else:                       vat_const_rate = ""

vat_cap_c = pd.read_csv( "data/vat/" + "vat-for-capitulo-c.csv"
                       , encoding = "latin1"
            ) . rename( columns = { "CODE" : "25-broad-categs"
                                  , "DESCRIPTION" : "description"
            } )
vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                        , sep = ";"
                        , encoding = "latin1" )

if vat_strategy == 'const': # short-circuit the vat-code keys; set everything to 19
  vat_cap_c[ "vat, min"] = vat_const_rate
  vat_cap_c[ "vat, max"] = vat_const_rate
  vat_coicop["vat, min"] = vat_const_rate
  vat_coicop["vat, max"] = vat_const_rate

for (vat,frac) in [ ("vat"    ,     "vat frac")
                  , ("vat, min", "vat frac, min")
                  , ("vat, max", "vat frac, max") ]:
  vat_cap_c[frac]  = vat_cap_c[vat]  / (1 + vat_cap_c[vat])
  vat_coicop[frac] = vat_coicop[vat] / (1 + vat_coicop[vat])

  # Multiplying vat-fraction by value (payment)
    # results in the fraction  of the value attributable to the vat.
    # For instance, if the VAT were 20%, then (0.2 / 1.2) is that fraction.


if True: # save
  suffix = vat_strategy + "_" + str(vat_const_rate)

  oio.saveStage(subsample, vat_coicop, 'vat_coicop_' + suffix )
  oio.saveStage(subsample, vat_cap_c,  'vat_cap_c_'  + suffix )

  vat_coicop = vat_coicop.drop( columns = ["description","Notes"] )
  vat_cap_c = vat_cap_c.drop( columns = ["description"] )

  oio.saveStage(subsample, vat_coicop, 'vat_coicop_brief_' + suffix )
  oio.saveStage(subsample, vat_cap_c, 'vat_cap_c_brief_'   + suffix )
