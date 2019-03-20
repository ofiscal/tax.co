import pandas as pd
import numpy as np

import python.common.util as util


def theTest():
  s = pd.Series( [1,1,2,2], index = [101,102,103,104] )
  nq = util.noisyQuantile( 4, 0, 0.001, s )
  return (  (nq[102] < nq[103]) # This is a partial order. We can say nothing,
          & (nq[101] < nq[103]) # for instance, about how 101 and 102 compare.
          & (nq[102] < nq[104])
          & (nq[101] < nq[104])
          & (len(nq) == 4) )
