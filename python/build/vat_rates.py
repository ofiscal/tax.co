# PURPOSE : This creates:
  # a bridge from 8-digit COICOP to VAT rate
  # a bridge from the 25 "capitulo c" codes to a VAT rate
  # two more, briefer versions of those two keys

import sys
import pandas as pd

import python.common.misc as c
import python.common.cl_args as c
import python.build.output_io as oio


vat_cap_c = pd.read_csv( "data/vat/" + "vat-for-capitulo-c.csv"
                       , encoding = "latin1"
            ) . rename( columns = { "CODE" : "25-broad-categs"
                                  , "DESCRIPTION" : "description"
            } )

vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                        , sep = ";" # TODO PITFALL
                        , encoding = "latin1" )

for (vat,frac) in [ ("vat"     , "vat frac")
                  , ("vat, min", "vat frac, min")
                  , ("vat, max", "vat frac, max") ]:
  # Multiplying vat-fraction by value (payment, price)
    # results in the fraction  of the value attributable to the vat.
    # For instance, if the VAT were 20%, then (0.2 / 1.2) is that fraction.
    # This is because reported expenditures are post-tax.
  vat_cap_c[frac]  = vat_cap_c[vat]  / (1 + vat_cap_c[vat])
  vat_coicop[frac] = vat_coicop[vat] / (1 + vat_coicop[vat])

if True: # save
  oio.saveStage( c.subsample
               , vat_coicop
               , 'vat_coicop.' + c.vat_strategy_suffix )
  oio.saveStage( c.subsample
               , vat_cap_c
               , 'vat_cap_c.'  + c.vat_strategy_suffix )

  vat_coicop = vat_coicop.drop( columns = ["description","Notes"] )
  vat_cap_c = vat_cap_c.drop( columns = ["description"] )

  oio.saveStage( c.subsample
               , vat_coicop
               , 'vat_coicop_brief.' + c.vat_strategy_suffix )
  oio.saveStage( c.subsample
               , vat_cap_c
               , 'vat_cap_c_brief.'   + c.vat_strategy_suffix )
