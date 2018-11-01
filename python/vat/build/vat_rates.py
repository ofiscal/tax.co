import sys
import pandas as pd

import python.vat.build.common as common
import python.vat.build.output_io as oio


# PITFALL|WART: If the vat_strategy is "approx" or "detail", this produces the same files,
# but saves them with different names. That's done so I can avoid using conditional logic
# in the Makefile.

vat_cap_c = pd.read_csv( "data/vat/" + "vat-for-capitulo-c.csv"
                       , encoding = "latin1"
            ) . rename( columns = { "CODE" : "25-broad-categs"
                                  , "DESCRIPTION" : "description"
            } )
vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                        , sep = ";"
                        , encoding = "latin1" )

if common.vat_strategy == 'const': # short-circuit the vat-code keys; set everything to 19
  vat_cap_c[ "vat, min"] = common.vat_flat_rate
  vat_cap_c[ "vat, max"] = common.vat_flat_rate
  vat_coicop["vat, min"] = common.vat_flat_rate
  vat_coicop["vat, max"] = common.vat_flat_rate

for (vat,frac) in [ ("vat"     , "vat frac")
                  , ("vat, min", "vat frac, min")
                  , ("vat, max", "vat frac, max") ]:
  vat_cap_c[frac]  = vat_cap_c[vat]  / (1 + vat_cap_c[vat])
  vat_coicop[frac] = vat_coicop[vat] / (1 + vat_coicop[vat])

  # Multiplying vat-fraction by value (payment)
    # results in the fraction  of the value attributable to the vat.
    # For instance, if the VAT were 20%, then (0.2 / 1.2) is that fraction.


if True: # save
  oio.saveStage( common.subsample
               , vat_coicop
               , 'vat_coicop.' + common.vat_strategy_suffix )
  oio.saveStage( common.subsample
               , vat_cap_c
               , 'vat_cap_c.'  + common.vat_strategy_suffix )

  vat_coicop = vat_coicop.drop( columns = ["description","Notes"] )
  vat_cap_c = vat_cap_c.drop( columns = ["description"] )

  oio.saveStage( common.subsample
               , vat_coicop
               , 'vat_coicop_brief.' + common.vat_strategy_suffix )
  oio.saveStage( common.subsample
               , vat_cap_c
               , 'vat_cap_c_brief.'   + common.vat_strategy_suffix )
