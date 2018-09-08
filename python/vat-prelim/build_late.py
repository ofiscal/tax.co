# The value-added tax.

import sys
import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
import python.vat.legends as vat_files
import python.vat.output_io as vat_output_io


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.
files = list( vat_files.purchase_file_legends.keys() )


purchases = vat_output_io.readStage(subsample,'/2.purchases,prices,taxes')
if True: # build the person expenditure data
  purchases["transactions"] = 1
  people = purchases.groupby(
    ['household', 'household-member'])['value','vat-paid',"transactions"].agg('sum')
  people = people.reset_index(level = ['household', 'household-member'])
  vat_output_io.saveStage(subsample, people, '/3.person-level-expenditures')


#people = vat_output_io.readStage(subsample, '3.person-level-expenditures')
if True: # merge demographic statistics
  # PITFALL: Even if using a subsample of purchases, use the complete demographic data sample
  demog = pd.read_csv( datafiles.yearSubsampleSurveyFolder(2017,1) + 'st2_sea_enc_per_csv.csv'
                    , usecols = list( vat_files.person_file_legend.keys() )
  )
  demog = demog.rename(columns=vat_files.person_file_legend) # homogenize column names across files


  if True: # normalize some categorical variables to be 0-1
    demog["female"] =   demog["female"] - 1          # orig 1=male,2=female
    demog["female"] =   demog["female"].map( {0:False,1:True} )
    demog["student"] =  demog["student"]  * (-1) + 2 # orig 1=student,2=not
    demog["student"] =  demog["student"].map( {0:False,1:True} )
    demog["literate"] = demog["literate"] * (-1) + 2 # orig 1=lit,2=not
    demog["literate"] = demog["literate"].map( {0:False,1:True} )
    demog["r-indig"] =    demog["race"] == 1
    demog["r-git|rom"] =  demog["race"] == 2
    demog["r-raizal"] =   demog["race"] == 3
    demog["r-palenq"] =   demog["race"] == 4
    demog["r-neg|mul"] =  demog["race"] == 5
    demog["r-whi|mest"] = demog["race"] == 6

  edu_key = { 1 : "Ninguno",
      2 : "Preescolar",
      3 : "Basica\n Primaria",
      4 : "Basica\n Secundaria",
      5 : "Media",
      6 : "Superior o\n Universitaria",
      9 : "No sabe,\n no informa" }
  demog["education"] = pd.Categorical(
    demog["education"].map( edu_key ),
    categories = list( edu_key.values() ),
    ordered = True)

  vat_output_io.saveStage(subsample, demog, '/4.demog')

  people = pd.merge( people, demog, how = "right"
                     , on=["household","household-member"] )
  people["value/inc"] = people["value"]/people["income"]
  people["vat/value"] = people["vat-paid"]/people["value"]
  people["vat/inc"] = people["vat-paid"]/people["income"]

  del(demog)

  people["age-decile"] = pd.qcut(
    people["age"], 10, labels = False, duplicates='drop')
  people["income-decile"] = pd.qcut(
    people["income"], 10, labels = False, duplicates='drop')
  people["vat/income"] = people["vat-paid"] / people["income"]
  people["value/income"] = people["value"] / people["income"]
  people["education"] = pd.Series(
    pd.Categorical( people["education"], ordered=True) )

  vat_output_io.saveStage(subsample, people, '/5.person-demog-expenditures')


# people = vat_output_io.readStage(subsample, '/5.person-demog-expenditures')
if True: # aggregate from household-members to households
  people["members"] = 1
  h_sum = people.groupby(
      ['household']
    ) ['value','vat-paid',"transactions","income","members"
    ] . agg('sum')
  h_min = people.groupby(
      ['household']
    ) ['age','female'
    ] . agg('min'
    ) . rename( columns = {'age' : 'age-min',
                           'female' : 'has-male',
    } )
  h_min["has-male"] = 1 - h_min["has-male"]
  h_max = people.groupby(
      ['household']
    ) ['age','literate','student','female','education',
       'r-indig', 'r-git|rom', 'r-raizal', 'r-palenq', 'r-whi|mest'
    ] . agg('max'
    ) . rename( columns = {'age' : 'age-max',
                           'literate' : 'has-lit',
                           'student' : 'has-student',
                           'education' : 'edu-max',
                           'female' : 'has-female',
                           'r-indig' : 'has-indig',
                           'r-git|rom' : 'has-git|rom',
                           'r-raizal' : 'has-raizal',
                           'r-palenq' : 'has-palenq',
                           'r-whi|mest' : 'has-whi|mest'
    } )
  households = pd.concat( [h_sum,h_min,h_max]
                         , axis=1 )

  households["value/inc"] = households["value"]/households["income"]
  households["vat/value"] = households["vat-paid"]/households["value"]
  households["vat/inc"] = households["vat-paid"]/households["income"]

  households["household"] = households.index
    # when there are multiple indices, reset_index is the way to do that

  households["has-child"] = households["age-min"] < 18
  households["has-elderly"] = households["age-max"] > 65

  households["income-decile"] = pd.qcut(
    households["income"], 10, labels = False, duplicates='drop')

  households["vat/income"] = households["vat-paid"] / households["income"]
  households["value/income"] = households["value"] / households["income"]

  vat_output_io.saveStage(subsample, households, '/6.households')

# households = vat_output_io.readStage(subsample, '/6.households')
if True: # data sets derived from households
  if True: # households with income
    households_w_income = households[ households["income"] > 0 ].copy()
      # Without the copy (even if I use .loc(), as suggested by the error)
      # this causes an error about modifying a view.
    households_w_income["income-decile"] = pd.qcut(
      households_w_income["income"], 10, labels = False, duplicates='drop')
    vat_output_io.saveStage(subsample, households_w_income,
                            '/7.households_w_income')

  if True: # summaries of the income deciles in two data sets
    households_w_income_decile_summary = \
      util.summarizeQuantiles("income-decile", households_w_income)
    vat_output_io.saveStage(subsample,
                            households_w_income_decile_summary,
                            '/8.households_w_income_decile_summary')

    households_decile_summary = \
      util.summarizeQuantiles("income-decile", households)
    vat_output_io.saveStage(subsample,
                            households_decile_summary,
                            '/9.households_decile_summary')
