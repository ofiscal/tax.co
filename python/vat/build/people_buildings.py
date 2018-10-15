import sys
import pandas as pd

import python.vat.build.output_io as oio


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.

buildings = oio.readStage(subsample, '/buildings')
people = oio.readStage(subsample, '/people')

people = pd.merge( people, buildings
                 , how = "left"
                 , on="household" )

oio.saveStage(subsample, people, '/people_buildings')
