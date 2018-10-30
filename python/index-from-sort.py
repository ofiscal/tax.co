import pandas as pd


df = pd.DataFrame( [ [ 0, 55, 3, 122 ]
                   , [ 1,  1, 1,   2 ] ]
                  , index = ["income","household"]
                 ) . transpose()

grouped = df.groupby('household')

def sort_household_by_income_then_make_index(df):
  dff = df.sort_values("income", ascending = False)
  dff["member-by-income"] = range(1, len(dff) + 1)
  return dff

x = grouped . apply( sort_household_by_income_then_make_index
          ) . drop( columns = "household"
          ) . reset_index( # the top level of the index shares the name "household" and is equal to it
          ) . drop( columns = "level_1" ) # the other part of the index is unneeded

# By this point x is already a single data frame.

