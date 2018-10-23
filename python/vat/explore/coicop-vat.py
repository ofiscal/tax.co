import pandas as pd
import numpy as np

import python.vat.build.output_io as oio


subsample = 10
purchases = oio.readStage( subsample, "purchases_2_vat" )

# When I check purchases[ purchases["coicop"] == x ] for these x,
# the results are consistent with the coicop-vat bridge.
# 11110103, 11110104, 11110105
# 1119807, 1119808, 1119809
# 1180103, 1180201, 1180301
