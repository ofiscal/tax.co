# The value-added tax.

import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
import python.vat.files as vat_files
import python.vat.output_io as vat_output_io


subsample = 100 # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.
files = list( vat_files.purchase_file_legends.keys() )


if True: # build the purchase data
  purchases = pd.DataFrame() # will accumulate from each file
  for file in files:
    legend = vat_files.purchase_file_legends[file]
    shuttle = pd.read_csv(
      datafiles.yearSubsampleSurveyFolder(2017,subsample) + file + '.csv'
      , usecols = list( legend.keys() )
    )
    shuttle = shuttle.rename(columns=legend) # homogenize column names across files
    shuttle["file-origin"] = file
  
    if False: # print summary stats for `shuttle`, before merging with `purchases`
      print( "\n\nFILE: " + file + "\n" )
      for colname in shuttle.columns.values:
        col = shuttle[colname]
        print("\ncolumn: " + colname)
        print("missing: " + str(len(col.index)-col.count())
              + " / "  + str(len(col.index)))
        print( col.describe() )

    purchases = purchases.append(shuttle)
  del(shuttle)
  vat_output_io.saveStage(subsample, purchases, '/1.purchases')


if True: # merge coicop, build money-valued variables
  coicop_vat = pd.read_csv( "data/vat/coicop-vat.csv", sep=';' )
  purchases = purchases.merge( coicop_vat, on="coicop" )

  purchases["price"] = purchases["value"] / purchases["quantity"]
  purchases["1-value"] = purchases["value"]
  purchases["1-quantity"] = purchases["quantity"]
  purchases["frequency"].replace( vat_files.frequency_legend, inplace=True )
  purchases["value"] = purchases["frequency"] * purchases["value"]
  purchases["vat-paid"] = purchases["value"] * purchases["vat-rate"]

  vat_output_io.saveStage(subsample, purchases, '/2.purchases,prices,taxes')


# purchases = vat_output_io.readStage(subsample,'/2.purchases,prices,taxes')
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
    demog["student"] =  demog["student"]  * (-1) + 2 # orig 1=student,2=not
    demog["literate"] = demog["literate"] * (-1) + 2 # orig 1=lit,2=not
    demog["r-indig"] =    demog["race"] == 1
    demog["r-git|rom"] =  demog["race"] == 2
    demog["r-raizal"] =   demog["race"] == 3
    demog["r-palenq"] =   demog["race"] == 4
    demog["r-neg|mul"] =  demog["race"] == 5
    demog["r-whi|mest"] = demog["race"] == 6
  vat_output_io.saveStage(subsample, demog, '/4.demog')

  people = pd.merge( people, demog, how = "right"
                     , on=["household","household-member"] )
  people["value/inc"] = people["value"]/people["income"]
  people["vat/val"] = people["vat-paid"]/people["value"]
  people["vat/inc"] = people["vat-paid"]/people["income"]

  del(demog)
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
  households["vat/val"] = households["vat-paid"]/households["value"]
  households["vat/inc"] = households["vat-paid"]/households["income"]

  households["household"] = households.index
    # when there are multiple indices, reset_index is the way to do that
  vat_output_io.saveStage(subsample, households, '/6.households')

# households = vat_output_io.readStage(subsample, '/6.households')
