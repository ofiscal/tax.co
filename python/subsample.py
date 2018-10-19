# At times this is memory intensive. My OS kept killing it, until I ran it with nothing else going on
# -- closed my browsers and all other docker containers. (I left Emacs, Dolphin and a few Konsoles open.)

import os
import pandas as pd

import python.datafiles as datafiles


folder = datafiles.yearSurveyFolder(2017)

def find_input(name):
  return folder + "orig/csv/" + name + '.csv'


if True: # read, subsample households
  households_filename = "Viviendas_y_hogares"
  print("now (henceforth) processing: " + households_filename)
  households = pd.read_csv( find_input( households_filename )
                          , usecols = ["DIRECTORIO"] # DIRECTORIO = household
                          , sep = ";"
  )

  household_samples = {1 : households}
  for denom in [10,100,1000]:
    household_samples[ denom ] = households.sample( frac = 1/denom )


if True: ## Subsample the rest of the ENPH
  names = list( set( datafiles.files[2017] ) - set( {households_filename} ) )

  for subsample in [1,10,100,1000]:
    subfolder = folder + "recip-" + str(subsample)
    if not os.path.exists( subfolder ):
      os.makedirs( subfolder )

  for name in names:
    print("now (henceforth) processing: " + name)
    data = pd.read_csv(folder + "orig/csv/" + name + '.csv', sep=";")

    for subsample in [1,10,100,1000]:
      if subsample == 1: # skip a pointless merge
            shuttle = data
      else: shuttle = pd.merge( data
                              , household_samples[subsample]
                              , on="DIRECTORIO" )
      shuttle.to_csv(
        folder + "recip-" + str(subsample) + "/" + name + ".csv" )
