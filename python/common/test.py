from  pandas.util.testing import assert_frame_equal

def afe(df1,df2):
  return assert_frame_equal( df1, df2, check_names=False)

