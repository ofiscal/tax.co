import sys
import pandas as pd
import numpy as np

import python.util as util
import python.vat.build.output_io as oio
from python.vat.build.people.files import edu_key


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.

people = oio.readStage( subsample, "people_3_purchases" )

people["education"] = util.interpretCategorical( people["education"]
                                               , edu_key.values() )

if True: # aggregate from household members to households
  people["members"] = 1
  h_first = people.groupby( ['household']
    ) ['region-1','region-2','estrato' # these are constant within household
    ] . agg('first')
  h_sum = people.groupby(
      ['household']
    ) [  'value','vat paid, min','vat paid, max', 'transactions','income','members'
       , 'income, pension'
       , 'income, cesantia'
       , 'income, capital, dividends'
       , 'income, capital w/o dividends'
       , 'income, infrequent'
       , 'income, govt'
       , 'income, private'
       , 'income, labor'
    ] . agg('sum')
  h_min = people.groupby(
      ['household']
    ) ['age','female'
    ] . agg('min'
    ) . rename( columns = {'age' : 'age-min',
                           'female' : 'has-male',
    } )
  h_min["has-male"] = 1 - h_min["has-male"] # TODO ? asymmetric
  h_max = people.groupby(
      ['household']
    ) ['age','literate','student','female','female head','education',
       'race, indig', 'race, git|rom', 'race, raizal', 'race, palenq', 'race, whi|mest'
    ] . agg('max'
    ) . rename( columns = {'age' : 'age-max',
                           'literate' : 'has-lit',
                           'student' : 'has-student',
                           'education' : 'edu-max',
                           'female' : 'has-female',
                           'race, indig' : 'has-indig',
                           'race, git|rom' : 'has-git|rom',
                           'race, raizal' : 'has-raizal',
                           'race, palenq' : 'has-palenq',
                           'race, whi|mest' : 'has-whi|mest'
    } )
  households = pd.concat( [h_first,h_sum,h_min,h_max]
                        , axis=1 )

  households["vat/value, min"] = households["vat paid, min"]/households["value"]
  households["vat/value, max"] = households["vat paid, max"]/households["value"]
  households["vat/income, min"] = households["vat paid, min"]/households["income"]
  households["vat/income, max"] = households["vat paid, max"]/households["income"]
  households["value/income"] = households["value"]/households["income"]

  households["household"] = households.index
    # when there are multiple indices, reset_index is the way to do that

  # TODO : < 10 also interesting, because work legal at age 10 or more
    # 10 or above in rural, 12 or above urban
  households["has-child"] = households["age-min"] < 18
  households["has-elderly"] = households["age-max"] > 65

  households["income-decile"] = pd.qcut(
    households["income"], 10, labels = False, duplicates='drop')


if True: # data sets derived from households
  if True: # households with income
    households_w_income = households[ households["income"] > 0 ].copy()
      # Without the copy (even if I use .loc(), as suggested by the error)
      # this causes an error about modifying a view.
    households_w_income["income-decile"] = pd.qcut(
      households_w_income["income"], 10, labels = False, duplicates='drop')

  if True: # summaries of the income deciles in two data sets
    households_w_income_decile_summary = \
      util.summarizeQuantiles("income-decile", households_w_income)

    households_decile_summary = \
      util.summarizeQuantiles("income-decile", households)


if True: # save
  oio.saveStage(subsample, households
                       , 'households' )
  oio.saveStage(subsample, households_w_income
                       , 'households_w_income' )
  oio.saveStage(subsample, households_w_income_decile_summary
                       , 'households_w_income_decile_summary' )
  oio.saveStage(subsample, households_decile_summary
                       , 'households_decile_summary' )
