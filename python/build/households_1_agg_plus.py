# PURPOSE
#########
# Aggregate from persons to households.
# Compute some more variables.

if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.common as com
  import python.common.describe as desc
  import python.common.util as util
  import python.build.output_io as oio
  from   python.build.people.files import edu_key
  import python.build.households_1_agg_plus_defs as defs


if True: # input
  ppl = oio.readStage(
    com.subsample,
    "people_3_income_taxish." + com.strategy_year_suffix )
  ppl["edu"] = util.interpretCategorical(
    ppl["edu"],
    edu_key.values() )

if True: # compute five columns for top five member incomes
  ppl["(rank, labor income) = 1"] = (
    ppl["income, labor"] * (ppl["rank, labor income"] == 1) )
  ppl["(rank, labor income) = 2"] = (
    ppl["income, labor"] * (ppl["rank, labor income"] == 2) )
  ppl["(rank, labor income) = 3"] = (
    ppl["income, labor"] * (ppl["rank, labor income"] == 3) )
  ppl["(rank, labor income) = 4"] = (
    ppl["income, labor"] * (ppl["rank, labor income"] == 4) )
  ppl["(rank, labor income) = 5"] = (
    ppl["income, labor"] * (ppl["rank, labor income"] == 5) )


if True: # aggregate from household members to households
  ppl["members"] = 1 # will be summed
  h_first = ppl.groupby( ["household"]
    ) [ defs.cols_const_within_hh
    ] . agg("first")
  h_sum = ( ppl.loc[ :, ( ["household","members"]
                        + defs.income_and_tax__person_level
                        + defs.cols_income_rank ) ]
          . groupby( "household" )
          . agg("sum") )
  h_min = ppl.groupby(
      ["household"]
    ) [["age", "female"]
    ] . agg("min"
    ) . rename( columns = {"age"    : "age-min",
                           "female" : "has-male",
    } )
  h_min["has-male"] = 1 - h_min["has-male"]
    # If female is 0 for anyone in a household, then min(female) = 0,
    # i.e. the household includes a male.
  #
  if True: # Aggregating by max.
      # This is complicated by the categorical `edu` variable.
      # For some reason, if `edu` is missing for everyone in a household,
      # Pandas throws an error instead of defining max-edu = np.nan.
      # Therefore I handle the `edu` variable separately.
    cols_without_edu = ( defs.cols_to_max.copy() +
                         defs.income_and_spending__household_level )
      # PITFALL! Without the .copy() above, the next line
      # would modify defs.cols_to_max.
    cols_without_edu.remove("edu") # destructive side effect and no output
    edu_max = ( ppl
      [ ppl["edu"].notnull() ]
      . groupby( ["household"] )
      [[ "edu" ]]
      . agg("max")
      . rename( columns = { "edu" : "edu-max" } ) )
    other_max = ppl.groupby(
        ["household"]
      ) [ cols_without_edu
      ] . agg("max"
      ) . rename( columns = {
          "age"            : "age-max",
          "literate"       : "has-lit",
          "student"        : "has-student",
          "female"         : "has-female",
          "race, indig"    : "has-indig",
          "race, git|rom"  : "has-git|rom",
          "race, raizal"   : "has-raizal",
          "race, palenq"   : "has-palenq",
          "race, whi|mest" : "has-whi|mest"
      } )
    h_max = pd.concat( [edu_max, other_max],
                       axis = 1 )
    del( edu_max, other_max )

if True: # Assemble the aggregates, then compute a few variables.
  households = pd.concat( [h_first, h_sum, h_min, h_max]
                        , axis=1 )
  households["household"]   = households.index
    # when there are multiple indices, reset_index is the way to do that
  households["has-child"]   = households["age-min"] < 18
  households["all-elderly"] = households["age-min"] > 65
  households["has-elderly"] = households["age-max"] > 65
  #
  # PITFALL: Income decile and percentile for persons exist too. They are different.
  households["income-decile"] = (
    util.noisyQuantile( 10, 0, 1, households["income"] ) )
  households["income-percentile"] = (
    util.noisyQuantile( 100, 0, 1, households["income"] ) )
  households["one"] = 1 # used in report/households.py to create the trivial partition.
    # TODO ? move to report/households.py
  households_decile_summary = desc.summarizeQuantiles(
      "income-decile", households)

if True: # save
  oio.saveStage( com.subsample, households
               , "households_1_agg_plus." + com.strategy_year_suffix )
  oio.saveStage( com.subsample, households_decile_summary
               , "households_decile_summary." + com.strategy_year_suffix )
