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
  who = {
    "one: 1"                            : "all",
    "income-decile: 0"                  : "income %ile 0-9",
    "income-decile: 1"                  : "income %ile 10-19",
    "income-decile: 2"                  : "income %ile 20-29",
    "income-decile: 3"                  : "income %ile 30-39",
    "income-decile: 4"                  : "income %ile 40-49",
    "income-decile: 5"                  : "income %ile 50-59",
    "income-decile: 6"                  : "income %ile 60-69",
    "income-decile: 7"                  : "income %ile 70-79",
    "income-decile: 8"                  : "income %ile 80-89",
    "income-percentile-in[90,97]: True" : "income %ile 90-97",
    "income-percentile: 98"             : "income %ile 98",
    "income-percentile: 99"             : "income %ile 99" }

if True:
  dfs = {}
  def select_from( file : str ) -> pd.DataFrame:
    return ( pd.read_csv( overviews_dir + file,
                          index_col = "Unnamed: 0" )
             [list(who.keys())] .
             rename(columns=who) .
             loc[stats] .
             transpose() )
  normal = select_from( "/overview.detail.2018.csv" )
  holiday = select_from( "/overview.vat_holiday_3.2018.csv" )
  dfs["normal"] = normal
  dfs["holiday"] = holiday

for k in ["normal","holiday"]:
  dfs[k]["vat paid: mean"] = (
    0.5 * ( dfs[k]["vat paid, min: mean"] +
            dfs[k]["vat paid, max: mean"] ) )
  dfs[k] = dfs[k].drop( columns = [ "vat paid, min: mean",
                                    "vat paid, max: mean" ] )

shift_window = 180
  # If people can shift their purchase times by a month,
  # then effectively the VAT holiday is two months,
  # regardless of how long it is by law.

if True: # build report on income groups
  by_income = (
    pd.concat(
      [ ( dfs["normal"] .
          rename( columns = {"vat paid: mean":"normal"} ) ),
        ( dfs["holiday"] .
          rename( columns = {"vat paid: mean":"holiday"} ) ) ],
      axis = "columns" ) )
  by_income["mix"] = (1/365) * (
    (365 - shift_window) * dfs["normal"] +
           shift_window  * dfs["holiday"]  )
  by_income["saved"] = (
    by_income["normal"] - by_income["mix"] )
  by_income["saved, %"] = 100 * (
    by_income["saved"] /  by_income["normal"] )
  by_income

if True: # build federal VAT income report
  vat_revenue_2017 = 59917589707522 # about 6e13
  by_person_normal = by_income.loc["all","normal"]
  federal = by_income.loc["all"] * vat_revenue_2017 / by_person_normal
  federal

