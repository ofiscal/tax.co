import sys
import pandas as pd

import python.vat.build.output_io as oio
import python.vat.build.common as common


buildings = oio.readStage(common.subsample, '/buildings')
people = oio.readStage(common.subsample, '/people_1')

people = pd.merge( people, buildings
                 , how = "left"
                 , on="household" )

oio.saveStage(common.subsample, people, '/people_2_buildings')
