import sys
import pandas as pd

import python.vat.build.output_io as oio
import python.vat.build.legends as legends
import python.util as util

subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.


if True: # input files
  # This data set is too big unless I down-cast the numbers.
  purchases = oio.readStage( subsample
                           , "purchases_1_5_no_origin"
                           , dtype = {
                               "25-broad-categs" : "float32"
                             , "coicop" : "float32"
                             , "freq" : "float32"
                             , "household" : "int32"
                             , "household-member" : "int32"
                             , "is-purchase" : "float32"
                             , "quantity" : "float32"
                             , "value" : "float32"
                             , "weight" : "float32"
                             , "where-got" : "float32"
                           } )
  vat_cap_c = oio.readStage( subsample
                           , "vat_cap_c_brief"
                           , dtype = {
                             "25-broad-categs" : "int32"
                             , "vat" : "float32"
                             , "vat, min" : "float32"
                             , "vat, max" : "float32"
                             , "vat frac" : "float32"
                             , "vat frac, min" : "float32"
                             , "vat frac, max" : "float32"
                           } )
  vat_coicop = oio.readStage( subsample
                            , "vat_coicop_brief"
                            , dtype = {
                                "coicop" : "int32"
                              , "vat" : "float32"
                              , "vat, min" : "float32"
                              , "vat, max" : "float32"
                              , "vat frac" : "float32"
                              , "vat frac, min" : "float32"
                              , "vat frac, max" : "float32"
                            } )


if True: # add VAT to COICOP-labeled purchases
  if True: # use the primary bridge
    purchases_coicop = purchases.merge( vat_coicop, how = "left", on="coicop" )


if True: # add VAT to capitulo-c-labeled purchases
  purchases_cap_c = purchases.merge( vat_cap_c, how = "left", on="25-broad-categs" )
  purchases = purchases_coicop . combine_first( purchases_cap_c )


if True: # compute a few more variables
  purchases["freq-code"] = purchases["freq"]
    # kept for the sake of drawing a table of purchase frequency
    # with frequencies spread evenly across the x-axis
  purchases["freq"].replace( legends.freq
                           , inplace=True )
  purchases = purchases.drop(
    purchases[ purchases["freq"].isnull() ]
    .index
  )

  purchases["value"] = purchases["freq"] * purchases["value"]
  purchases["vat paid, max"] = purchases["value"] * purchases["vat frac, max"]
  purchases["vat paid, min"] = purchases["value"] * purchases["vat frac, min"]

  oio.saveStage(subsample, purchases, 'purchases_2_vat')
