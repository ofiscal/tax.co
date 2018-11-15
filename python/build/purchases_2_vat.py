import sys
import pandas as pd
import numpy as np

import python.build.output_io as oio
import python.build.legends as legends
import python.util as util
import python.build.common as common


if True: # input files
  # This data set is too big unless I down-cast the numbers.
  purchases = oio.readStage( common.subsample
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

  vat_cap_c = oio.readStage( common.subsample
                           , "vat_cap_c_brief." + common.vat_strategy_suffix
                           , dtype = {
                             "25-broad-categs" : "int32"
                             , "vat" : "float32"
                             , "vat, min" : "float32"
                             , "vat, max" : "float32"
                             , "vat frac" : "float32"
                             , "vat frac, min" : "float32"
                             , "vat frac, max" : "float32"
                           } )

  vat_coicop = oio.readStage( common.subsample
                            , "vat_coicop_brief." + common.vat_strategy_suffix
                            , dtype = {
                                "coicop" : "int32"
                              , "vat" : "float32"
                              , "vat, min" : "float32"
                              , "vat, max" : "float32"
                              , "vat frac" : "float32"
                              , "vat frac, min" : "float32"
                              , "vat frac, max" : "float32"
                            } )

  if common.vat_strategy == "prop-2018-11-31":
    vat_coicop_2_digit = pd.read_csv( "python/build/vat_prop.2018_11_31/2-digit.csv" )
    vat_coicop_3_digit = pd.read_csv( "python/build/vat_prop.2018_11_31/3-digit.csv" )

    # PITFALL: We want to replace 1 in the VAT rate columns, but not in the coicop-prefix columns.
    # This replaces both, then restores the original prefixes.
    orig_key_2_digit = vat_coicop_2_digit["coicop-2-digit"]
    orig_key_3_digit = vat_coicop_3_digit["coicop-3-digit"]
    vat_coicop_2_digit = vat_coicop_2_digit.replace(1, float(common.vat_flat_rate))
    vat_coicop_3_digit = vat_coicop_3_digit.replace(1, float(common.vat_flat_rate))
    vat_coicop_2_digit["coicop-2-digit"] = vat_coicop_2_digit
    vat_coicop_3_digit["coicop-3-digit"] = vat_coicop_3_digit

  else: # Always read, but the only way these are used is if vat_strategy is approx.
    vat_coicop_2_digit = pd.read_csv( "python/build/vat_approx/2-digit.csv" )
    vat_coicop_3_digit = pd.read_csv( "python/build/vat_approx/3-digit.csv" )

if True: # add columns to the coicop-prefix bridges
  vat_coicop_2_digit["vat frac, min"] = vat_coicop_2_digit[ "vat, min"
                                      ] . apply( lambda x: x / (1+x) )
  vat_coicop_2_digit["vat frac, max"] = vat_coicop_2_digit[ "vat, max"
                                      ] . apply( lambda x: x / (1+x) )
  vat_coicop_3_digit["vat frac, min"] = vat_coicop_3_digit[ "vat, min"
                                      ] . apply( lambda x: x / (1+x) )
  vat_coicop_3_digit["vat frac, max"] = vat_coicop_3_digit[ "vat, max"
                                      ] . apply( lambda x: x / (1+x) )

if True: # left-pad every coicop value (including coicop prefixes) with 0s
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
  if common.vat_strategy in ["approx","prop-2018-11-31"]:
    purchases_2_digit = purchases.merge( vat_coicop_2_digit, how = "left"
                          , on="coicop-2-digit" )
    purchases_3_digit = purchases.merge( vat_coicop_3_digit, how = "left"
                          , on="coicop-3-digit" )
    purchases_coicop = purchases_2_digit . combine_first( purchases_3_digit )
  else: # PITFALL: For both const and detail strategies, use the primary bridge
    purchases_coicop = purchases.merge( vat_coicop, how = "left", on="coicop" )

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
  purchases["vat paid, min"] = purchases["value"] * purchases["vat frac, min"]
  purchases["vat paid, max"] = purchases["value"] * purchases["vat frac, max"]

  oio.saveStage(common.subsample, purchases, "purchases_2_vat." + common.vat_strategy_suffix )
