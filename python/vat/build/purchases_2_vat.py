import sys
import pandas as pd
import numpy as np

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

  vat_coicop_2_digit = pd.read_csv( "python/vat/build/vat_approx/2-digit.csv" )
  vat_coicop_3_digit = pd.read_csv( "python/vat/build/vat_approx/3-digit.csv" )

if True: # 8-pad everything coicop-like
  purchases         ["coicop"] = util.pad_column_as_int( 8, purchases         ["coicop"] )
    # This creates some "00000nan" values. After creating 2- and 3-digit
    # prefixes, we can turn those back into NaN.
  vat_coicop        ["coicop"] = util.pad_column_as_int( 8, vat_coicop        ["coicop"] )
  vat_coicop_2_digit["coicop-2-digit"] = (
    util.pad_column_as_int( 2, vat_coicop_2_digit["coicop-2-digit"] ) )
  vat_coicop_3_digit["coicop-3-digit"] = (
    util.pad_column_as_int( 3, vat_coicop_3_digit["coicop-3-digit"] ) )
  purchases["coicop-2-digit"] = purchases["coicop"] . apply( lambda s: s[0:2] )
  purchases["coicop-3-digit"] = purchases["coicop"] . apply( lambda s: s[0:3] )

  purchases.loc[ purchases["coicop"] . str.contains( "[^0-9]" )
               , "coicop"
               ] = np.nan
  purchases.loc[ purchases["coicop"] . isnull()
               , "coicop-2-digit"
               ] = np.nan
  purchases.loc[ purchases["coicop"] . isnull()
               , "coicop-3-digit"
               ] = np.nan


if True: # add vat to coicop-labeled purchases

  # PITFALL: The following are alternatives. Use only one.

  if True: # use the primary bridge
    purchases_coicop = purchases.merge( vat_coicop, how = "left", on="coicop" )

  if False: # merge on the 2- and 3-digit approximations instead
    purchases_2_digit = purchases.merge( vat_coicop_2_digit, how = "left"
                          , on="coicop-2-digit"
                      ) . drop( columns = ["coicop_y"] )
    purchases_3_digit = purchases.merge( vat_coicop_3_digit, how = "left"
                          , on="coicop-3-digit"
                      ) . drop( columns = ["coicop_y"] )
    purchases_coicop = purchases_2_digit . combine_first( purchases_3_digit )

if True: # add vat to capitulo-c-labeled purchases
  purchases_cap_c = purchases.merge( vat_cap_c, how = "left", on="25-broad-categs" )
  purchases = purchases_coicop . combine_first( purchases_cap_c )

if False: # drop anything missing min vat (which implies max also missing)
  purchases = purchases[ ~ purchases["vat, min"] . isnull() ]

if True: # handle freq, value, vat paid
  purchases["freq-code"] = purchases["freq"]
    # Kept for the sake of drawing a table of purchase frequency,
    # with frequencies spread evenly across the x-axis.
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
