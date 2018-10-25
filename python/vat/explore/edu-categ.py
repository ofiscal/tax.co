import sys
import pandas as pd

import python.util as util
import python.vat.build.output_io as oio
from python.vat.build.people.files import edu_key
import python.vat.build.common as common


people = oio.readStage( common.subsample, "people_3_purchases" )
households = oio.readStage( common.subsample, "households" )
purchase_sums = oio.readStage( common.subsample, "purchase_sums" )

if False: people["education"] = pd.Categorical( people["education"]
                , categories = list( edu_key.values() )
                , ordered = True)

people["education"] = util.interpretCategorical( people["education"], edu_key.values() )

