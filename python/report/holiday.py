if True:
  import sys
  import pandas as pd
  #
  import python.common.terms as t
  import python.common.common as c

if True: # bearings
  overviews_dir = "output/vat/tables/recip-" + str(c.subsample)
  stats = ["vat paid, min: mean",
           "vat paid, max: mean"]
  who = [ "one: 1",
          "income-decile: 0",
          "income-decile: 1",
          "income-decile: 2",
          "income-decile: 3",
          "income-decile: 4",
          "income-decile: 5",
          "income-decile: 6",
          "income-decile: 7",
          "income-decile: 8",
          "income-percentile-in[90,97]: True",
          "income-percentile: 98",
          "income-percentile: 99" ]

if True:
  def select_from( file : str ) -> pd.DataFrame:
    return ( pd.read_csv( overviews_dir + file,
                          index_col = "Unnamed: 0" )
             [who] .
             loc[stats] .
             transpose() )
  normal = select_from( "/overview.detail.2018.csv" )
  holiday = select_from( "/overview.vat_holiday_3.2018.csv" )
  dfs = [normal,holiday]

for df in dfs:
  df["vat paid: mean"] = (
    0.5 * ( df["vat paid, min: mean"] +
            df["vat paid, max: mean"] ) )

