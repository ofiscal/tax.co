# PURPOSE : This creates:
  # a bridge from 8-digit COICOP to VAT rate
  # a bridge from the 25 "capitulo c" codes to a VAT rate
  # two more, briefer versions of those two keys

import sys
import pandas as pd

import python.build.common as common
import python.build.output_io as oio


# PITFALL|WART: For many values of common.vat_strategy, this produces the same files,
# but saves them with different names. Moreover often they go unused downstream.
# That's done so I can avoid using conditional logic in the Makefile.
# They are small files, so the processing and memory cost is negligible. (It's about 1s of CPU time.)

vat_cap_c = pd.read_csv( "data/vat/" + "vat-for-capitulo-c.csv"
                       , encoding = "latin1"
            ) . rename( columns = { "CODE" : "25-broad-categs"
                                  , "DESCRIPTION" : "description"
            } )

if common.vat_strategy == "finance_ministry":
      vat_coicop = pd.read_csv( "python/build/vat_finance_ministry/" + "vat-by-coicop.csv"
                              , sep = ","
                              , encoding = "latin1" )
elif common.vat_strategy == "prop_2018_11_29":
      vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.prop-2018-11-29.csv"
                              , sep = ";"
                              , encoding = "latin1" )
else: vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                              , sep = ";" # TODO PITFALL
                              , encoding = "latin1" )

if True: # Replacements, if appropriate
  vat_columns = ["vat", "vat, min", "vat, max"]
  if common.vat_strategy == 'detail_224': # one proposal is to replace the 19% with 22.4%
    for vc in vat_columns:
      vat_cap_c[vc]  = vat_cap_c[vc]  . replace( 0.19, 0.224 )
      vat_coicop[vc] = vat_coicop[vc] . replace( 0.19, 0.224 )

  if common.vat_strategy == 'const': # short-circuit the vat-code keys; set everything to 19
    for vc in vat_columns:
      vat_cap_c[vc]  = common.vat_flat_rate
      vat_coicop[vc] = common.vat_flat_rate

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

  vat_coicop = vat_coicop.drop( columns = ["description"] )
  if common.vat_strategy != 'finance_ministry':
    vat_coicop = vat_coicop.drop( columns = ["Notes"] )
  vat_cap_c = vat_cap_c.drop( columns = ["description"] )

  oio.saveStage( common.subsample
               , vat_coicop
               , 'vat_coicop_brief.' + common.vat_strategy_suffix )
  oio.saveStage( common.subsample
               , vat_cap_c
               , 'vat_cap_c_brief.'   + common.vat_strategy_suffix )
