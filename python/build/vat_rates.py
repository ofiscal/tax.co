# PURPOSE
#########
# This program creates:
#   a bridge from 8-digit COICOP to VAT rate
#   a bridge from the 25 "capitulo c" codes to a VAT rate
#   two more, briefer versions of those two keys

if True:
  import sys
  import pandas as pd
  #
  import python.common.terms as t
  import python.common.common as c
  import python.common.misc as misc
  import python.build.output_io as oio

vat_cap_c = (
    misc . read_csv_or_xlsx (
        c . vat_by_capitulo_c
        , encoding = "latin1" ) .
    rename (
        columns = { "CODE" : "25-broad-categs"
                  , "DESCRIPTION" : "description" }
    ) )

vat_coicop = (
    misc . read_csv_or_xlsx (
        c . vat_by_coicop
        , encoding = "latin1" )
    . rename (
        columns = { "CODE" : "coicop" } ) )

for (vat,frac) in [ ("vat"     , "vat frac")
                  , ("vat, min", "vat frac, min")
                  , ("vat, max", "vat frac, max") ]:
  # Multiplying vat-fraction by value (payment, price)
    # results in the fraction  of the value attributable to the vat.
    # For instance, if the VAT were 20%, then (0.2 / 1.2) is that fraction.
    # This is because reported expenditures are post-tax.
  vat_cap_c [frac] = vat_cap_c [vat] / (1 + vat_cap_c [vat])
  vat_coicop[frac] = vat_coicop[vat] / (1 + vat_coicop[vat])

if True: # save
  oio.saveStage( c.subsample
               , vat_coicop
               , 'vat_coicop.' + c.strategy_suffix )
  oio.saveStage( c.subsample
               , vat_cap_c
               , 'vat_cap_c.'  + c.strategy_suffix )

  vat_coicop = vat_coicop.drop( columns = ["DESCRIPTION"] )
  vat_cap_c  = vat_cap_c .drop( columns = ["description"] )

  oio.saveStage( c.subsample
               , vat_coicop
               , 'vat_coicop_brief.' + c.strategy_suffix )
  oio.saveStage( c.subsample
               , vat_cap_c
               , 'vat_cap_c_brief.'   + c.strategy_suffix )
