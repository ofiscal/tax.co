# The value-added tax.

import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
import python.vat.files as vatfiles
import os


subsample = 1 # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.
purchases = pd.DataFrame() # will accumulate from each file
files = list( vatfiles.purchase_file_legends.keys() )

def saveStage(data,name):
  path = 'output/vat-data/recip-' + str(subsample)
  if not os.path.exists(path): os.makedirs(path)
  data.to_csv( path + '/' + name + ".csv" )

def readStage(name): # to skip rebuilding something
  path = 'output/vat-data/recip-' + str(subsample)
  return pd.read_csv( path + '/' + name + ".csv" )


if True: # build the purchase data
  for file in files:
    legend = vatfiles.purchase_file_legends[file]
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
  saveStage(purchases, '/1.purchases')


if True: # merge coicop, build money-valued variables
  coicop_vat = pd.read_csv( "data/vat/coicop-vat.csv", sep=';' )
  purchases = purchases.merge( coicop_vat, on="coicop" )

  purchases["price"] = purchases["value"] / purchases["quantity"]
  purchases["1-value"] = purchases["value"]
  purchases["1-quantity"] = purchases["quantity"]
  purchases["frequency"].replace( vatfiles.frequency_legend, inplace=True )
  purchases["value"] = purchases["frequency"] * purchases["value"]
  purchases["vat-paid"] = purchases["value"] * purchases["vat-rate"]

  saveStage(purchases, '/2.purchases,prices,taxes')


# purchases = readStage('/2.purchases,prices,taxes')
if True: # build the person expenditure data
  purchases["transactions"] = 1
  people = purchases.groupby(
    ['household', 'household-member'])['value','vat-paid',"transactions"].agg('sum')
  people = people.reset_index(level = ['household', 'household-member'])
  saveStage(people, '/3.person-level-expenditures')
  

#people = readStage('/3.person-level-expenditures')
if True: # merge demographic statistics
  # PITFALL: Even if using a subsample of purchases, use the complete demographic data sample
  demog = pd.read_csv( datafiles.yearSubsampleSurveyFolder(2017,1) + 'st2_sea_enc_per_csv.csv'
                    , usecols = list( vatfiles.person_file_legend.keys() )
  )
  demog = demog.rename(columns=vatfiles.person_file_legend) # homogenize column names across files

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
  saveStage(demog, '/4.demog')

  people = pd.merge( people, demog, how = "right"
                     , on=["household","household-member"] )
  people["val/inc"] = people["value"]/people["income"]
  people["vat/val"] = people["vat-paid"]/people["value"]
  people["vat/inc"] = people["vat-paid"]/people["income"]

  del(demog)
  saveStage(people, '/5.person-demog-expenditures')


# people = readStage('/5.person-demog-expenditures')
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

  households["val/inc"] = households["value"]/households["income"]
  households["vat/val"] = households["vat-paid"]/households["value"]
  households["vat/inc"] = households["vat-paid"]/households["income"]

  households["household"] = households.index
    # when there are multiple indices, reset_index is the way to do that
  saveStage(households, '/6.households')

# households = readStage('/6.households')
