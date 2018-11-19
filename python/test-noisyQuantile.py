import pandas as pd
import numpy as np

import python.util as util

def theTest():
  s = pd.Series( [1,1,2,2] )
  nq = util.noisyQuantile( 4, 0, 0.01, s )
  return (nq[1] < nq[2]) & (len(nq) == 4)
