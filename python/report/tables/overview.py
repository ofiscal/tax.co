# exec( open( "python/report/tables/overview.py" ) . read() )

import os
import sys
import pandas as pd

import python.common.util as util
import python.draw.util as draw
import python.build.output_io as oio
import python.common.misc as c
import python.common.cl_args as cl


output_dir = "output/vat/tables/recip-" + str(cl.subsample) + "/"
if not os.path.exists(output_dir): os.makedirs(output_dir)


if True: # Get, prepare the data
  households = oio.readStage( cl.subsample, "households."        + cl.vat_strategy_suffix )

  households["income, labor + cesantia"] = households["income, labor"] + households["income, cesantia"]

  households["income-percentile-in[90,97]"] = (
      (households["income-percentile"] >= 90)
    & (households["income-percentile"] <= 97) )

  households["income < min wage"] = (
    households["income"] < c.min_wage )

if True: # create a summary dataframe
  householdVars = [
      "income < min wage"
    , "pension, receiving"
    , "pension, contributing (if not pensioned)"
    , "pension, contributor(s) (if not pensioned) = split"
    , "pension, contributor(s) (if not pensioned) = self"
    , "pension, contributor(s) (if not pensioned) = employer"
    , "seguro de riesgos laborales (if reported)"
    , "income"
    , "income, labor + cesantia"
    , "income, capital"
    , "income, dividend"
    , "income, pension"
    , "income, govt"
    , "income, private"
    , "income, infrequent"
    , "income, rank 1"
    , "income, rank 2"
    , "income, rank 3"
    , "income, rank 4"
    , "income, rank 5"
    , "income, labor, rank 1"
    , "income, labor, rank 2"
    , "income, labor, rank 3"
    , "income, labor, rank 4"
    , "income, labor, rank 5"
    , "members"
    , "female head"
    , "value"
    , "value/income"
    , "vat paid, min"
    , "vat paid, max"
    , "vat/income, min"
    , "vat/income, max"
    , "vat/value, min"
    , "vat/value, max"
    , "predial"
    , "tax, pension"
    , "tax, pension, employer"
    , "tax, salud"
    , "tax, salud, employer"
    , "tax, solidaridad"
    , "tax, parafiscales"
    , "tax, cajas de compensacion"
    , "cesantias + primas"
    , "tax, gmf"
    , "tax, ganancia ocasional"
    , "tax, indemnizacion"
    , "tax, donacion"
    , "tax, income, labor + pension"
    , "tax, income, capital + non-labor"
    , "tax, dividend"
    ]

  householdGroupVars = [ "one"
                       , "female head"
                       , "income-decile"
                       , "income-percentile"
                       , "income-percentile-in[90,97]"
                       , "region-2" ]

  # PITFALL: Earlier, this looped over two data sets, households and people.
  # Now its outermost loop is unnecessary.
  summaryDict = {}
  for (unit, df, vs, gvs) in [
      ( "households", households, householdVars, householdGroupVars ) ]:

    groupSummaries = []
    for gv in gvs:
      varSummaries = []
      for v in vs:
        t = util.tabulate_stats_by_group( df, gv, v, "weight" )
        t = t.rename(
          columns = dict( zip( t.columns
                              , map( lambda x: v + ": " + x
                                   , t.columns ) ) )
          , index    = dict( zip( t.index
                                , map( lambda x: str(gv) + ": " + str(x)
                                     , t.index ) ) )
                    )
        varSummaries . append( t )
      groupSummaries . append( pd.concat( varSummaries, axis = 1 ) )
    summaryDict[unit] = pd.concat( groupSummaries, axis = 0 )

  df_tmi = pd.concat( list( summaryDict.values() ), axis = 0
                    ) . transpose()


if True: # save
  df_tmi.to_csv( output_dir      + "overview, tmi." + cl.vat_strategy_suffix + ".csv" )
  draw.to_latex( df_tmi, output_dir, "overview, tmi." + cl.vat_strategy_suffix )


if True: # do the same thing to a subset of that data
  df = df_tmi.loc[[
      "income < min wage: mean"
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
    , "seguro de riesgos laborales (if reported): mean"
    , "seguro de riesgos laborales (if reported): min"
    , "seguro de riesgos laborales (if reported): max"
    , "income: mean"
    , "income: min"
    , "income: max"
    , "income, labor + cesantia: mean"
    , "income, capital: mean"
    , "income, dividend: mean"
    , "income, pension: mean"
    , "income, govt: mean"
    , "income, private: mean"
    , "income, infrequent: mean"
    , "income, rank 1: mean"
    , "income, rank 1: mean_nonzero"
    , "income, rank 2: mean"
    , "income, rank 2: mean_nonzero"
    , "income, rank 3: mean"
    , "income, rank 3: mean_nonzero"
    , "income, rank 4: mean"
    , "income, rank 4: mean_nonzero"
    , "income, rank 5: mean"
    , "income, rank 5: mean_nonzero"
    , "income, labor, rank 1: mean"
    , "income, labor, rank 1: mean_nonzero"
    , "income, labor, rank 2: mean"
    , "income, labor, rank 2: mean_nonzero"
    , "income, labor, rank 3: mean"
    , "income, labor, rank 3: mean_nonzero"
    , "income, labor, rank 4: mean"
    , "income, labor, rank 4: mean_nonzero"
    , "income, labor, rank 5: mean"
    , "income, labor, rank 5: mean_nonzero"
    , "members: mean"
    , "female head: mean"
    , "value: median_unweighted"
    , "value: mean"
    , "vat paid, min: mean"
    , "vat paid, max: mean"
    , "value/income: median_unweighted"
    , "value/income: mean"
    , "vat/value, min: median_unweighted"
    , "vat/value, min: mean"
    , "vat/value, max: median_unweighted"
    , "vat/value, max: mean"
    , "vat/income, min: median_unweighted"
    , "vat/income, min: mean"
    , "vat/income, max: median_unweighted"
    , "vat/income, max: mean"
    , "predial: median_unweighted"
    , "predial: mean"
    , "tax, pension: median_unweighted"
    , "tax, pension: mean"
    , "tax, pension, employer: median_unweighted"
    , "tax, pension, employer: mean"
    , "tax, salud: median_unweighted"
    , "tax, salud: mean"
    , "tax, salud, employer: median_unweighted"
    , "tax, salud, employer: mean"
    , "tax, solidaridad: median_unweighted"
    , "tax, solidaridad: mean"
    , "tax, parafiscales: median_unweighted"
    , "tax, parafiscales: mean"
    , "tax, cajas de compensacion: median_unweighted"
    , "tax, cajas de compensacion: mean"
    , "cesantias + primas: median_unweighted"
    , "cesantias + primas: mean"
    , "tax, gmf: median_unweighted"
    , "tax, gmf: mean"
    , "tax, ganancia ocasional: median_unweighted"
    , "tax, ganancia ocasional: mean"
    , "tax, indemnizacion: median_unweighted"
    , "tax, indemnizacion: mean"
    , "tax, donacion: median_unweighted"
    , "tax, donacion: mean"
    , "tax, income, labor + pension: median_unweighted"
    , "tax, income, labor + pension: mean"
    , "tax, income, capital + non-labor: median_unweighted"
    , "tax, income, capital + non-labor: mean"
    , "tax, dividend: median_unweighted"
    , "tax, dividend: mean"
  ]]

  df.to_csv(         output_dir + "overview." + cl.vat_strategy_suffix + ".csv" )
  draw.to_latex( df, output_dir, "overview." + cl.vat_strategy_suffix )
