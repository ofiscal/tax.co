import pandas as pd
import pandas.util.testing as pdt

# This is obsolete; in recent versions of pandas, you can just use
# x.equals(y). And it's better, because it does not impose NaN != NaN.
#
# def assert_same_data( x, y ):
#   if type(x) == pd.core.series.Series:
#     pdt.assert_series_equal( x, y )
#   else:
#     pdt.assert_frame_equal( x, y, check_names=False)
