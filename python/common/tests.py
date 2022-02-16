import pandas as pd
import python.common.common as com
import python.common.util as util


def test_quantiles( df : pd.DataFrame ) -> ():
  for (col,top) in [ ("income-decile",    10),
                     ("income-percentile",100) ]:
    assert df[col] . min() == 0
    assert df[col] . max() == top - 1
    if com.subsample != 1000:
      assert util.near( df[col] . mean(),
                        (top - 1) / 2 )