import pandas as pd
import numpy as np

import python.build.output_io as oio
import python.build.legends as legends
import python.common.util as util
import python.common.misc as c
import python.common.cl_args as c


if True: # input files
  # This data set is too big unless we down-cast the numbers.
  purchases = oio.readStage (
      c.subsample
    , "purchases_1"
    , dtype = { "25-broad-categs" : "float32"
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

  vat_cap_c = oio.readStage( c.subsample
                           , "vat_cap_c_brief." + c.strategy_suffix
                           , dtype = {
                             "25-broad-categs" : "int32"
                             , "vat" : "float32"
                             , "vat, min" : "float32"
                             , "vat, max" : "float32"
                             , "vat frac" : "float32"
                             , "vat frac, min" : "float32"
                             , "vat frac, max" : "float32"
                           } )

  vat_coicop = oio.readStage( c.subsample
                            , "vat_coicop_brief." + c.strategy_suffix
                            , dtype = {
                                "coicop" : "int32"
                              , "vat" : "float32"
                              , "vat, min" : "float32"
                              , "vat, max" : "float32"
                              , "vat frac" : "float32"
                              , "vat frac, min" : "float32"
                              , "vat frac, max" : "float32"
                            } )

if True: # left-pad every coicop value with 0s
  purchases  ["coicop"] = util.pad_column_as_int( 8, purchases  ["coicop"] )
  vat_coicop ["coicop"] = util.pad_column_as_int( 8, vat_coicop ["coicop"] )

if True: # add these columns: ["vat", "vat, min", "vat, max"]
  purchases_coicop = purchases.merge(
    vat_coicop, how = "left", on="coicop" )
  purchases_cap_c = purchases.merge(
    vat_cap_c,  how = "left", on="25-broad-categs" )
  purchases = purchases_coicop . combine_first( purchases_cap_c )

if True: # motorcycles are special
  purchases["big-hog"] = (1 * (purchases["coicop"]=="07120101")
                            * (purchases["value"]>(9e6) ) )
  purchases.loc[ purchases["big-hog"]>0, "vat"]      = 0.27
  purchases.loc[ purchases["big-hog"]>0, "vat, min"] = 0.27
  purchases.loc[ purchases["big-hog"]>0, "vat, max"] = 0.27

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

  purchases["value"]         = purchases["freq"] *  purchases["value"]
  purchases["vat paid, min"] = purchases["value"] * purchases["vat frac, min"]
  purchases["vat paid, max"] = purchases["value"] * purchases["vat frac, max"]

  oio.saveStage( c.subsample, purchases, "purchases_2_vat." + c.strategy_suffix )
