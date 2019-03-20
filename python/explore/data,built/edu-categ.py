import sys
import pandas as pd

import python.common.util as util
import python.build.output_io as oio
from python.build.people.files import edu_key
import python.common.misc as c
import python.common.cl_args as c


people = oio.readStage( c.subsample, "people_3_purchases" )
households = oio.readStage( c.subsample, "households" )
purchase_sums = oio.readStage( c.subsample, "purchase_sums" )

if False: people["education"] = pd.Categorical( people["education"]
                , categories = list( edu_key.values() )
                , ordered = True)

people["education"] = util.interpretCategorical( people["education"], edu_key.values() )

