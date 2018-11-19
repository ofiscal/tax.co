import pandas as pd
import numpy as np

import python.util as util


def theTest():
  s = pd.Series( [1,1,2,2], index = [5,55,555,1515] )
  nq = noisyQuantile2( 4, 0, 0.001, s )
  return (nq[1] < nq[2]) & (len(nq) == 4)
