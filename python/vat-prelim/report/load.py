import sys
import os

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

import python.util as util
import python.datafiles as datafiles
import python.vat.files as vatfiles
import python.vat.output_io as oio
import python.draw.util as draw

from matplotlib.ticker import EngFormatter

subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.
vat_pics_dir = "output/vat-pics/recip-" + str(subsample) + "/"
if not os.path.exists(vat_pics_dir): os.makedirs(vat_pics_dir)
