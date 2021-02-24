# PURPOSE
#########
# Compute VAT per purchase in the purchase data.

if True:
  import numpy as np
  import pandas as pd
  #
  import python.build.classes           as cla
  import python.build.output_io         as oio
  import python.build.purchases.legends as legends
  import python.common.common           as c
  import python.common.util             as util


if True: # input files
  purchases = oio.readStage (
    # Data is too big unless we down-cast the numbers
    # from 64-bit to 32-bit.
      c.subsample
    , "purchases_1"
    , dtype = { "25-broad-categs"  : "float32"
              , "coicop"           : "float32"
              , "per month"        : "float32"
              , "household"        : "int32"
              , "household-member" : "int32"
              , "is-purchase"      : "float32"
              , "quantity"         : "float32"
              , "value"            : "float32"
              , "weight"           : "float32"
              , "where-got"        : "float32"
    } )
  #
  vat_cap_c = oio.readStage(
      c.subsample
    , "vat_cap_c_brief." + c.strategy_suffix
    , dtype = {
      "25-broad-categs" : "int32"
      , "vat"           : "float32"
      , "vat, min"      : "float32"
      , "vat, max"      : "float32"
      , "vat frac"      : "float32"
      , "vat frac, min" : "float32"
      , "vat frac, max" : "float32"
    } )
  #
  vat_coicop = oio.readStage(
      c.subsample
    , "vat_coicop_brief." + c.strategy_suffix
    , dtype = {
      "coicop"          : "int32"
      , "vat"           : "float32"
      , "vat, min"      : "float32"
      , "vat, max"      : "float32"
      , "vat frac"      : "float32"
      , "vat frac, min" : "float32"
      , "vat frac, max" : "float32"
    } )

if True: # left-pad every coicop value with 0s
  purchases  ["coicop"] = util.pad_column_as_int(
    8, purchases  ["coicop"] )
  vat_coicop ["coicop"] = util.pad_column_as_int(
    8, vat_coicop ["coicop"] )

if True: # add these columns: ["vat", "vat, min", "vat, max"]
  # The tax laws do not precisely conform to the COICOP labeling of goods.
  # We (especially our tax policy expert, David Suarez)
  # had to exercise our judgment,
  # determining what VAT rate applied to which COICOP category.
  # In some cases the VAT was clear. In other cases,
  # we recorded minimum and maximum possible VAT values.
  # The columns "vat, min", "vat max", "vat frac, min" and "vat frac, max"
  # correspond to those minima and maxima.
  purchases_coicop = purchases.merge(
    vat_coicop, how = "left", on="coicop" )
  purchases_cap_c = purchases.merge(
    vat_cap_c,  how = "left", on="25-broad-categs" )
  purchases = purchases_coicop . combine_first( purchases_cap_c )

if True: # Big motorcycles are special. We proxy for "big" with "expensive".
  purchases["big-hog"] = (1 * (purchases["coicop"]=="07120101")
                            * (purchases["value"]>(9e6) ) )
  for col in ["vat", "vat, min", "vat, max"]:
      purchases.loc[ purchases["big-hog"]>0, col] = 0.27
  for col in ["vat frac", "vat frac, min", "vat frac, max"]:
      purchases.loc[ purchases["big-hog"]>0, col] = 0.27 / 1.27

if False: # drop anything missing min vat (which implies max also missing)
  purchases = purchases[ ~ purchases["vat, min"] . isnull() ]

if True: # handle freq, value, vat paid
  purchases["freq-code"] = purchases["per month"]
    # Kept for the sake of drawing a table of purchase frequency,
    # with frequencies spread evenly across the x-axis.
  ( purchases["per month"] # PITFALL: not functional; the "inplace" option
                           # causes replace() to have no return value.
  . replace( legends.freq
           , inplace=True ) )

  purchases["value"]         = purchases["per month"] * purchases["value"]
  purchases["vat paid, min"] = purchases["value"]     * purchases["vat frac, min"]
  purchases["vat paid, max"] = purchases["value"]     * purchases["vat frac, max"]

oio.saveStage(
  c.subsample,
  purchases,
  "purchases_2_vat." + c.strategy_suffix )
