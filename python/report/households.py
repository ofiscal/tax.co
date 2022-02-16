# exec( open( "python/report/households.py" ) . read() )

if True:
  import os
  import sys
  import pandas as pd
  from itertools import chain
  #
  import python.build.output_io as oio
  import python.common.common as com
  import python.common.describe as desc
  import python.common.misc as c
  import python.draw.util as draw
  import python.report.defs as defs
  if   com.regime_year == 2016:
      import python.regime.r2016 as regime
  elif com.regime_year == 2018:
      import python.regime.r2018 as regime
  else:
      import python.regime.r2019 as regime


if True: # load data
  households = oio.readStage(
      com.subsample,
      "households_2_purchases." + com.strategy_year_suffix )

  earners = oio.readStage(
      com.subsample,
      "people_4_post_households." + com.strategy_year_suffix )

if True: # Create a few columns missing in the input data.
         # TODO ? Move upstream.
  for df in [households, earners]:
    df["income, labor + cesantia"] = (
        df["income, labor"]
        + df["income, cesantia"] )

    df["income-percentile-in[90,97]"] = (
        (df["income-percentile"] >= 90)
      & (df["income-percentile"] <= 97) )

    df["income < min wage"] = (
      df["income"] < c.min_wage )

if True: # create a summary dataframe
  commonVars = ( [
      "income < min wage"
    , "pension, receiving"
    , "pension, contributing (if not pensioned)"
    , "pension, contributor(s) (if not pensioned) = split"
    , "pension, contributor(s) (if not pensioned) = self"
    , "pension, contributor(s) (if not pensioned) = employer"
    , "seguro de riesgos laborales"
    , "income"
    , "income, labor + cesantia"
    , "income, rental + interest"
    , "income, dividend"
    , "income, pension"
    , "income, govt"
    , "income, private"
    , "income, infrequent"
    , "female head"
    , "value, purchase"
    , "purchase value / income"
    , "vat paid"
    , "vat / income"
    , "vat / purchase value"
    , "value, tax, predial" ]

    + regime.income_tax_columns +

    [ "tax, ss, pension"
    , "tax, ss, pension, employer"
    , "tax, ss, salud"
    , "tax, ss, salud, employer"
    , "tax, ss, solidaridad"
    , "tax, ss, parafiscales"
    , "tax, ss, cajas de compensacion"
    , "cesantias + primas"
    , "tax, income, gmf"
    , "tax, income, ganancia ocasional"
    ] )

  householdSpecificVars = [
    "(rank, labor income) = 1",
    "(rank, labor income) = 2",
    "(rank, labor income) = 3",
    "(rank, labor income) = 4",
    "(rank, labor income) = 5",
    "members",
    ]

  householdVars = commonVars + householdSpecificVars
  earnerVars    = commonVars

  commonRestrictedVars = (
    [ "income < min wage: mean"
    , "pension, receiving: mean"
    , "pension, receiving: min"
    , "pension, receiving: max"
    , "pension, contributing (if not pensioned): mean"
    , "pension, contributing (if not pensioned): min"
    , "pension, contributing (if not pensioned): max"
    , "pension, contributor(s) (if not pensioned) = split: mean"
    , "pension, contributor(s) (if not pensioned) = split: min"
    , "pension, contributor(s) (if not pensioned) = split: max"
    , "pension, contributor(s) (if not pensioned) = self: mean"
    , "pension, contributor(s) (if not pensioned) = self: min"
    , "pension, contributor(s) (if not pensioned) = self: max"
    , "pension, contributor(s) (if not pensioned) = employer: mean"
    , "pension, contributor(s) (if not pensioned) = employer: min"
    , "pension, contributor(s) (if not pensioned) = employer: max"
    , "seguro de riesgos laborales: mean"
    , "seguro de riesgos laborales: min"
    , "seguro de riesgos laborales: max"
    , "income: mean"
    , "income: min"
    , "income: max"
    , "income, labor + cesantia: mean"
    , "income, rental + interest: mean"
    , "income, dividend: mean"
    , "income, dividend: share"
    , "income, pension: mean"
    , "income, govt: mean"
    , "income, private: mean"
    , "income, infrequent: mean"
    , "female head: mean"
    , "value, purchase: median_unweighted"
    , "value, purchase: mean"
    , "vat paid: mean"
    , "purchase value / income: median_unweighted"
    , "purchase value / income: mean"
    , "vat / purchase value: median_unweighted"
    , "vat / purchase value: mean"
    , "vat / income: median_unweighted"
    , "vat / income: mean"
    , "value, tax, predial: median_unweighted"
    , "value, tax, predial: mean" ]

    # "chain.from_iterable" concatenates lists
    + list( chain.from_iterable( [ [ c + ": median_unweighted"
                                   , c + ": mean" ]
                                   for c in regime.income_tax_columns ] ) )
    +

    [ "tax, ss, pension: median_unweighted"
    , "tax, ss, pension: mean"
    , "tax, ss, pension, employer: median_unweighted"
    , "tax, ss, pension, employer: mean"
    , "tax, ss, salud: median_unweighted"
    , "tax, ss, salud: mean"
    , "tax, ss, salud, employer: median_unweighted"
    , "tax, ss, salud, employer: mean"
    , "tax, ss, solidaridad: median_unweighted"
    , "tax, ss, solidaridad: mean"
    , "tax, ss, parafiscales: median_unweighted"
    , "tax, ss, parafiscales: mean"
    , "tax, ss, cajas de compensacion: median_unweighted"
    , "tax, ss, cajas de compensacion: mean"
    , "cesantias + primas: median_unweighted"
    , "cesantias + primas: mean"
    , "tax, income, gmf: median_unweighted"
    , "tax, income, gmf: mean"
    , "tax, income, ganancia ocasional: median_unweighted"
    , "tax, income, ganancia ocasional: mean"
    ] )

  householdSpecificRestrictedVars = [
    "(rank, labor income) = 1: mean",
    "(rank, labor income) = 1: mean_nonzero",
    "(rank, labor income) = 2: mean",
    "(rank, labor income) = 2: mean_nonzero",
    "(rank, labor income) = 3: mean",
    "(rank, labor income) = 3: mean_nonzero",
    "(rank, labor income) = 4: mean",
    "(rank, labor income) = 4: mean_nonzero",
    "(rank, labor income) = 5: mean",
    "(rank, labor income) = 5: mean_nonzero",
    "members: mean",
    ]

  householdRestrictedVars = commonRestrictedVars + householdSpecificRestrictedVars
  earnerRestrictedVars    = commonRestrictedVars

  groupVars = [ "one"
              , "female head"
              , "income-decile"
              , "income-percentile"
              , "income-percentile-in[90,97]"
              , "region-2" ]

  # PITFALL: Earlier, this looped over two data sets, households and people.
  # Now its outermost loop could be flattened.
  summaryDict = {}
  for ( unit,         df,         vs,           ) in [
      ( "households", households, householdVars ) ]:

    groupSummaries = []
    for gv in groupVars:
      varSummaries = []
      for v in vs:
        t = desc.tabulate_stats_by_group( df, gv, v, "weight" )
        t = t.rename (
          columns = dict(
                zip( t.columns
                   , map( lambda x: v + ": " + x
                        , t.columns ) ) )
          , index = dict(
                zip( t.index
                   , map( lambda x: str(gv) + ": "
                          + defs.maybeFill( gv, str(x) )
                        , t.index ) ) ) )
        varSummaries . append( t )
      groupSummaries . append( pd.concat( varSummaries, axis = 1 ) )
    summaryDict[unit] = pd.concat( groupSummaries, axis = 0 )

  df_tmi = pd.concat( list( summaryDict.values() ), axis = 0
                    ) . transpose()

if True: # do the same thing to a subset of that data
  df = df_tmi.loc [ householdRestrictedVars ]

df_tmi . reset_index ( inplace = True )
df_tmi = df_tmi . rename ( columns = {"index" : "measure"} )
df     . reset_index ( inplace = True )
df     = df . rename ( columns = {"index" : "measure"} )

if True: # save
  oio.saveStage(
      com.subsample,
      df_tmi,
      "report_households_tmi." + com.strategy_year_suffix )
  oio.saveStage_excel(
      com.subsample,
      df_tmi,
      "report_households_tmi." + com.strategy_year_suffix )
  oio.saveStage(
      com.subsample,
      df,
      "report_households." + com.strategy_year_suffix )
  oio.saveStage_excel(
      com.subsample,
      df,
      "report_households." + com.strategy_year_suffix )
