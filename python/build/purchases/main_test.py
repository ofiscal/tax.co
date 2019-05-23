import numpy as np
import pandas as pd

import python.build.purchases.main_defs as defs


def test_drop_if_coicop_or_value_invalid():
  df = pd.DataFrame( { "coicop"          : [1, 1,      np.nan]
                     , "25-broad-categs" : [1, 1,      np.nan]
                     , "value"           : [1, np.nan, 1     ] } )
  assert ( ( defs.drop_if_coicop_or_value_invalid( df )
           == pd.DataFrame( { "coicop"          : [1]
                            , "25-broad-categs" : [1]
                            , "value"           : [1] } )  )
         . all() . all() )

if True: # run the tests
  test_drop_if_coicop_or_value_invalid()
