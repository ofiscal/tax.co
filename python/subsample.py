# PURPOSE
#########
# The code takes a long time to proceses the full data set.
# These subsamples speed up the development cycle,
# by allowing you to run the process on less data.
# There are 1/1, 1/10, 1/100 and 1/1000 subsamples.

# PITFALL
#########
# This is memory intensive. Depending on your hardware,
# it might not run without first killing other big apps.

# HOW TO USE IT
###############
# From the command line:
#   If calling Python directly,
#     select a subsample by setting
#     the first command-line argument to the denominator of one
#     of the above fractions. The Makefile contains a number of examples.
#   If calling Python via make,
#     see bash/make-all-models.sh for appropriate syntax.
#   If calling make via bash/make-all-models.sh,
#     see the header comment in that file.
# From the Python reepl:
#   Change the subsample value imported by common.py,
#   by changing common/params/repl.py.

if True:
  import os
  import pandas as pd
  import numpy as np
  #
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
  for subsample in [1,10,100,1000]:
    if subsample==1: household_index_samples[ subsample
                       ] = household_indices
    else:            household_index_samples[ subsample
                       ] = household_indices.sample(
                               frac         = 1/subsample
                             , random_state = 0 ) # seed


if True: ## Subsample each file (including Viviendas) based on that
  names = datafiles.files[2017]

  for subsample in [1,10,100,1000]:
    subfolder = folder + "recip-" + str(subsample)
    if not os.path.exists( subfolder ):
      os.makedirs( subfolder )

  for name in names:
    print("Processing " + name + ".")
    data = pd.read_csv(
      folder + "3_csv/" + name + '.csv' )
    for c in data.columns:
      if data[c].dtype == object:
        data[c] = ( data[c].astype(str)
                  . str.strip()
                  . replace( {'nan':np.nan} ) )

    for subsample in [1,10,100,1000]:
      if subsample == 1: # skip a pointless merge
            shuttle = data
      else: shuttle = pd.merge( data
                              , household_index_samples[subsample]
                              , on="DIRECTORIO" )
      shuttle.to_csv(
        folder + "recip-" + str(subsample) + "/" + name + ".csv" )
