import sys
import pandas as pd

import python.build.output_io as oio
import python.common.misc as c
import python.common.common as c


buildings = oio.readStage(
    1 # PITFALL: For buildings, we always use the full sample.
  , 'buildings'
  , dtype = {"estrato":'float64'}
)
people = oio.readStage(c.subsample, 'people_1')

people = pd.merge( people, buildings
                 , how = "left"
                 , on="household" )

oio.saveStage( c.subsample
             , people
             , 'people_2_buildings')
