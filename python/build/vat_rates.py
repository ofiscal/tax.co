# PURPOSE : This creates:
  # a bridge from 8-digit COICOP to VAT rate
  # a bridge from the 25 "capitulo c" codes to a VAT rate
  # two more, briefer versions of those two keys

if True:
  import sys
  import pandas as pd
  #
  import python.common.terms as t
  import python.common.common as c
  import python.build.output_io as oio

vat_cap_c = pd.read_csv( "data/vat/" + "vat-for-capitulo-c.csv"
                       , encoding = "latin1"
            ) . rename( columns = { "CODE" : "25-broad-categs"
                                  , "DESCRIPTION" : "description"
            } )

if True: # input
  if c.strategy == t.detail:
    vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                            , sep = ";" # TODO PITFALL
                            , encoding = "latin1" )
  elif c.strategy in [t.vat_holiday_1,
                      t.vat_holiday_2,
                      t.vat_holiday_3]:
    if True: # read the data
      if c.strategy in [t.vat_holiday_1,
                        t.vat_holiday_2]:
        vat_coicop = (
          pd.read_csv(
            "data/vat/holiday/" + "vat-by-coicop.csv" ) .
          drop( columns = ["Unnamed: 0"] ) )
      elif c.strategy in [t.vat_holiday_3]:
        vat_coicop = (
          pd.read_csv(
            "data/vat/holiday/" + "vat-by-coicop.ask_3.csv" ) .
          drop( columns = ["Unnamed: 0"] ) )
    if True: # un-Latinize the numbers
      vat_cols = ["vat","vat, min","vat, max"]
      vat_coicop.loc[:, vat_cols] = (
        vat_coicop.loc[:, vat_cols] .
        apply( ( lambda col:
                 col.str.replace( ",", "." ) .
                 astype( float ) ),
               axis = "rows" ) )
    if True: # set appropriate VAT rates to zero
      if c.strategy in [t.vat_holiday_1,
                        t.vat_holiday_3]:
        vat_coicop.loc[ vat_coicop["VAT Holiday"] == 1,
                        vat_cols ] = 0
      elif c.strategy == t.vat_holiday_2:
        vat_coicop.loc[ vat_coicop["VAT Holiday"] > 0,
                        vat_cols ] = 0
    vat_coicop = vat_coicop.drop(
      columns = ["VAT Holiday"] )

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

  vat_coicop = vat_coicop.drop( columns = ["description","Notes"] )
  vat_cap_c  = vat_cap_c .drop( columns = ["description"        ] )

  oio.saveStage( c.subsample
               , vat_coicop
               , 'vat_coicop_brief.' + c.strategy_suffix )
  oio.saveStage( c.subsample
               , vat_cap_c
               , 'vat_cap_c_brief.'   + c.strategy_suffix )

