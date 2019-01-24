import sys
import pandas as pd

import python.build.output_io as oio
import python.build.common as c


buildings = oio.readStage(c.subsample, 'buildings')
people = oio.readStage(c.subsample, 'people_1')

people = pd.merge( people, buildings
                 , how = "left"
                 , on="household" )

oio.saveStage(c.subsample, people, 'people_2_buildings')
