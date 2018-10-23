import sys
import pandas as pd

import python.util as util
import python.vat.build.output_io as oio
from python.vat.build.people.files import edu_key


subsample = 100 # int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.

people = oio.readStage( subsample, "people_3_purchases" )
households = oio.readStage( subsample, "households" )
purchase_sums = oio.readStage( subsample, "purchase_sums" )

if False: people["education"] = pd.Categorical( people["education"]
                , categories = list( edu_key.values() )
                , ordered = True)

people["education"] = util.interpretCategorical( people["education"], edu_key.values() )

