# PURPOSE
#########
# Aggregate from persons to households.
# Compute more variables.

if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.output_io as oio
  from python.build.people.files import edu_key
  import python.common.common as c
  #
  if c.regime_year == 2016:
    import python.regime.r2016 as regime
  else: import python.regime.r2018 as regime


ppl = oio.readStage(
  c.subsample,
  "people_4_income_taxish." + c.strategy_year_suffix )

ppl["education"] = util.interpretCategorical(
  ppl["education"],
  edu_key.values() )

if True: # compute five columns for top five member incomes
  ppl["income, rank 1"] = (
    ppl["income"] * (ppl["member-by-income"] == 1) )
  ppl["income, rank 2"] = (
    ppl["income"] * (ppl["member-by-income"] == 2) )
  ppl["income, rank 3"] = (
    ppl["income"] * (ppl["member-by-income"] == 3) )
  ppl["income, rank 4"] = (
    ppl["income"] * (ppl["member-by-income"] == 4) )
  ppl["income, rank 5"] = (
    ppl["income"] * (ppl["member-by-income"] == 5) )

  ppl["income, labor, rank 1"] = (
    ppl["income, labor"] * (ppl["member-by-income"] == 1) )
  ppl["income, labor, rank 2"] = (
    ppl["income, labor"] * (ppl["member-by-income"] == 2) )
  ppl["income, labor, rank 3"] = (
    ppl["income, labor"] * (ppl["member-by-income"] == 3) )
  ppl["income, labor, rank 4"] = (
    ppl["income, labor"] * (ppl["member-by-income"] == 4) )
  ppl["income, labor, rank 5"] = (
    ppl["income, labor"] * (ppl["member-by-income"] == 5) )


if True: # aggregate from household members to households
  ppl["members"] = 1 # will be summed
  h_first = ppl.groupby( ["household"]
    ) ["region-1", "region-2", "estrato", "weight" # these are constant within household
    ] . agg("first")
  many_vars = ( [ "members"
                , "transactions", "value"
                , "vat paid, min", "vat paid, max"
                , "predial"
                , "tax, ss, pension"
                , "tax, ss, pension, employer"
                , "tax, ss, salud"
                , "tax, ss, salud, employer"
                , "tax, ss, solidaridad"
                , "tax, ss, parafiscales"
                , "tax, ss, cajas de compensacion"
                , "cesantias + primas"
                , "tax, gmf"
                , "tax, ganancia ocasional" ]

                + regime.income_tax_columns +

                [ "income"
                , "income, pension"
                , "income, cesantia"
                , "income, dividend"
                , "income, capital (tax def)"
                , "income, infrequent"
                , "income, govt"
                , "income, private"
                , "income, labor"
                , "income, borrowing"
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
                ] )
  h_sum = ( ppl.loc[:, ["household"] + many_vars]
          . groupby( "household" )
          . agg("sum") )
  h_min = ppl.groupby(
      ["household"]
    ) ["age", "female"
    ] . agg("min"
    ) . rename( columns = {"age" : "age-min",
                           "female" : "has-male",
    } )
  h_min["has-male"] = 1 - h_min["has-male"]
    # If female is 0 for anyone in a household, then min(female) = 0,
    # i.e. the household includes a male.
  h_max = ppl.groupby(
      ["household"]
    ) [ "age", "literate", "student", "female", "female head", "education"
       , "race, indig", "race, git|rom", "race, raizal", "race, palenq", "race, whi|mest"
       , "pension, receiving"
       , "pension, contributing (if not pensioned)"
       , "pension, contributor(s) (if not pensioned) = split"
       , "pension, contributor(s) (if not pensioned) = self"
       , "pension, contributor(s) (if not pensioned) = employer"
       , "seguro de riesgos laborales"
    ] . agg("max"
    ) . rename( columns = {"age" : "age-max",
                           "literate" : "has-lit",
                           "student" : "has-student",
                           "education" : "edu-max",
                           "female" : "has-female",
                           "race, indig" : "has-indig",
                           "race, git|rom" : "has-git|rom",
                           "race, raizal" : "has-raizal",
                           "race, palenq" : "has-palenq",
                           "race, whi|mest" : "has-whi|mest"
    } )
  households = pd.concat( [h_first, h_sum, h_min, h_max]
                        , axis=1 )

  households["vat/value, min"]  = households["vat paid, min"]/households["value"]
  households["vat/value, max"]  = households["vat paid, max"]/households["value"]
  households["vat/income, min"] = households["vat paid, min"]/households["income"]
  households["vat/income, max"] = households["vat paid, max"]/households["income"]
  households["value/income"]    = households["value"]/households["income"]

  households["household"]   = households.index
    # when there are multiple indices, reset_index is the way to do that

  households["has-child"]   = households["age-min"] < 18
  households["has-elderly"] = households["age-max"] > 65

  # PITFALL: Income decile and percentile for persons exist too. They are different.
  households["income-decile"] = (
    util.noisyQuantile( 10, 0, 1, households["income"] ) )
  households["income-percentile"] = (
    util.noisyQuantile( 100, 0, 1, households["income"] ) )

  households["one"] = 1 # used to create the trivial partition

  households_decile_summary = util.summarizeQuantiles("income-decile", households)


if True: # save
  oio.saveStage( c.subsample, households
               , "households." + c.strategy_year_suffix )
  oio.saveStage( c.subsample, households_decile_summary
               , "households_decile_summary." + c.strategy_year_suffix )
