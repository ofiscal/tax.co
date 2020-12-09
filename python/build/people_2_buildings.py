# Merge the building data innto the person-level data.

import sys
import pandas as pd

import python.build.output_io as oio
import python.common.util as util
import python.common.common as common


if True: # merge people, buildings
  buildings = oio.readStage(
      1 # PITFALL: For buildings, we always use the full sample.
    , 'buildings'
    , dtype = {"estrato":'float64'}
  )
  people = oio.readStage(common.subsample, 'people_1')
  people = pd.merge( people, buildings
                   , how = "left"
                   , on="household" )

if True: # make some new variables
    people["age-decile"] = pd.qcut(
      people["age"], 10, labels = False, duplicates='drop')
    people["income-decile"] = (
      # PITFALL: there's a different such variable at the household level
      util.noisyQuantile( 10, 0, 1, people["income"] ) )
    people["female head"] = people["female"] * (people["household-member"]==1)

for ss in common . valid_subsamples:
    # PITFALL: Looping over subsample sizes because this program
    # always uses the full sample.
    # If it works, it works for all subsamples.
    oio.saveStage( ss
                 , people
                 , 'people_2_buildings')

