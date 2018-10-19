# At times this is memory intensive. My OS kept killing it, until I ran it with nothing else going on
# -- closed my browsers and all other docker containers. (I left Emacs, Dolphin and a few Konsoles open.)

import os
import pandas as pd

import python.datafiles as datafiles


folder = datafiles.yearSurveyFolder(2017)

def find_input(name):
  return folder + "orig/csv/" + name + '.csv'

if True: # read, subsample household indices
  print("Subsampling household indices (from Viviendas_y_hogares).")
  household_indices = pd.read_csv( find_input( "Viviendas_y_hogares" )
                                 , usecols = ["DIRECTORIO"] # DIRECTORIO = household
                                 , sep = ";" )
  household_index_samples = {}
  for subsample in [1,10,100,1000]:
    if subsample==1: household_index_samples[ subsample
                       ] = household_indices
    else:            household_index_samples[ subsample
                       ] = household_indices.sample( frac = 1/subsample )


if True: ## Subsample each file (including Viviendas) based on that
  names = datafiles.files[2017]

  for subsample in [1,10,100,1000]:
    subfolder = folder + "recip-" + str(subsample)
    if not os.path.exists( subfolder ):
      os.makedirs( subfolder )

  for name in names:
    print("Processing " + name + ".")
    data = pd.read_csv(folder + "orig/csv/" + name + '.csv', sep=";")

    for subsample in [1,10,100,1000]:
      if subsample == 1: # skip a pointless merge
            shuttle = data
      else: shuttle = pd.merge( data
                              , household_index_samples[subsample]
                              , on="DIRECTORIO" )
      shuttle.to_csv(
        folder + "recip-" + str(subsample) + "/" + name + ".csv" )
