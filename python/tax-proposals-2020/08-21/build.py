# PITFALL: This depends on some variables that were removed from python/build/
# in commit 2c82f5faad432aa1971bd940341adef2bf73ea02

# exec( open( "tax-proposal/2020-08-21/build.py" ) . read() )

if True:
  import os
  import sys
  import pandas as pd
  from itertools import chain
  #
  import python.build.output_io as oio
  import python.common.common as cl
  import python.common.misc as c
  import python.common.describe as desc
  import python.draw.util as draw

if cl.regime_year == 2016:
      import python.regime.r2016 as regime
else: import python.regime.r2018 as regime


if True: # Get, prepare the data
  hh = oio.readUserData(
      cl.subsample,
      "households_2_purchases." + cl.strategy_year_suffix )
  hh["income-percentile-in[90,97]"] = (
      (hh["income-percentile"] >= 90)
    & (hh["income-percentile"] <= 97) )
  hh["income < min wage"] = (
    hh["income"] < c.min_wage )

if True: # Sum the ss tax components, keep sum, drop components.
  ss_tax_components = [
      "tax, ss, pension"
    , "tax, ss, pension, employer"
    , "tax, ss, salud"
    , "tax, ss, salud, employer"
    , "tax, ss, solidaridad"
    , "tax, ss, parafiscales"
    , "tax, ss, cajas de compensacion"
    ]
  hh["tax, ss"] = hh[ss_tax_components].sum(axis="columns" )
  hh = hh.drop( columns = ss_tax_components )

if True: # Narrow the set of columns
  basicVars = ["household","weight"]
  groupVars = [
      "age-max"
    , "age-min"
    , "all-elderly"
    , "edu-max"
    , "estrato"
    , "female head"
    , "has-child"
    , "has-elderly"
    , "has-female"
    , "has-lit"
    , "has-male"
    , "has-student"
    , "household"
    , "income < min wage"
    , "income-decile"
    , "income-percentile"
    , "income-percentile-in[90,97]"
    , "members"
    , "one"
    , "pension, receiving"
    , "region-1"
    , "region-2"
    ]
  #
  taxVars = [
      "tax, income"
    , "tax, income, proposed"
    , "tax, income, most"
    , "tax, income, most, proposed"
    , "tax, income, dividend"
    , "tax, income, dividend, proposed"
    , "tax, income, inheritance, proposed"
    , "tax, income, ganancia ocasional"
    , "tax, income, ganancia ocasional, proposed" # PITFALL: omits inheritance
    , "tax, income, gmf"
    # , "value, purchase"
    # , "value, non-purchase"
    , "vat paid, max"
    # , "vat paid, min"
    , "value, tax, predial"
    , "value, tax, purchaselike non-predial non-VAT"
    , "value, tax, purchaselike non-VAT"
    # , "value, spending"
    # , "value, consumption"
    # , "vat / purchase value, min"
    # , "vat / purchase value, max"
    # , "vat / income, min"
    # , "vat / income, max"
    # , "purchase value / income"
    , "tax, ss" ]
  #
  incomeVars = [
      "income"
    # , "cesantias + primas"
    # , "income, cash"
    # , "income, in-kind"
    , "income, pension"
    # , "income, cesantia"
    , "income, dividend"
    , "income, capital (tax def)"
    , "income, infrequent"
    # , "income, govt"
    # , "income, private"
    , "income, labor"
    , "income, borrowing"
    ]
  #
  theVars = basicVars + groupVars + taxVars + incomeVars
  hh = hh[ basicVars + groupVars + taxVars + incomeVars ]

if True: # Compute total tax
  hh["tax"] = ( hh.loc[:, [ "tax, income"
                          , "vat paid, max"
                          , "value, tax, purchaselike non-VAT"
                          , "tax, ss" ] ] .
                sum(axis="columns" ) )
  hh["tax, proposed"] = ( hh.loc[:, [ "tax, income, proposed"
                                    , "vat paid, max"
                                    , "value, tax, purchaselike non-VAT"
                                    , "tax, ss" ] ] .
                          sum(axis="columns" ) )

taxVars = taxVars + ["tax", "tax, proposed"]
