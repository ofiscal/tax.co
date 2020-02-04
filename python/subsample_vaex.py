# Using Pandas, tax.co can throw memory errors.
# This file is an incomplete attempt at using Vaex instead,
# which processes on disk rather than in memory.
# (The memory errors are common in the early stages, through subsampling.
# After that I haven't run into them. So if I were to introduce Vaex,
# I might not need to propogate it any farther than the subsampling stage.)

import os
import numpy as np
import pandas as pd
import vaex

import python.build.datafiles as datafiles


folder = datafiles.yearSurveyFolder(2017)

def find_input(name):
  return folder + "3_csv/" + name + '.csv'

if True: # read, subsample household indices
  print("Subsampling household indices (from Viviendas_y_hogares).")
  household_indices = pd.read_csv(
      find_input( "Viviendas_y_hogares" )
    , usecols = ["DIRECTORIO"] ) # DIRECTORIO = household
  household_index_samples = {}
  household_index_samples_vaex = {}
  for subsample in [1,10,100,1000]:
    if subsample==1: household_index_samples[ subsample
                       ] = household_indices
    else:            household_index_samples[ subsample
                       ] = household_indices.sample(
                               frac         = 1/subsample
                             , random_state = 0 ) # seed
    household_index_samples_vaex[ subsample ] = (
      vaex.from_arrays(
        DIRECTORIO = # PITFALL: accepts any keyword
          household_index_samples[ subsample ]
          ["DIRECTORIO"] ) )

if True: ## Subsample each file (including Viviendas) based on that
  names = datafiles.files[2017]
  for subsample in [1,10,100,1000]:
    subfolder = folder + "recip-" + str(subsample)
    if not os.path.exists( subfolder ):
      os.makedirs( subfolder )
  for name in names:
    print("Processing " + name + ".")
    data = vaex.open(
      folder + "3_csv/" + name + '.csv' )
    for c in data.columns:
      if data[c].dtype == object:
        data[c] = ( data[c].astype(str)
                  . str.strip()
                  . replace( {'nan':np.nan} ) )

True
    for subsample in [1,10,100,1000]:
      if subsample == 1: # skip a pointless merge
            shuttle = data
      else: shuttle = pd.merge( data
                              , household_index_samples[subsample]
                              , on="DIRECTORIO" )
      shuttle.to_csv(
        folder + "recip-" + str(subsample) + "/" + name + ".csv" )
