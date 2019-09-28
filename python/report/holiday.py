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
  inflator = 1.0968321419999998
    # inflation index:
    #   2017-12: 138.853985
    #   2019-06: 147.1492953586
    #   => 5.97412 %
    # expected inflation in the next year: 3.5 %
    # => total inflation from 2017-12 to 2020-06:
    #   (1.0597412 * 1.035) = 1.0968321419999998

if True:
  dfs = {}
  def select_from( file : str ) -> pd.DataFrame:
    return ( pd.read_csv( overviews_dir + file,
                          index_col = "Unnamed: 0" )
             [list(who.keys())] .
             rename(columns=who) .
             loc[stats] .
             transpose() *
             inflator * # inflate from 2017-12 to 2020-06
             12 ) # switch from months to years
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

if True: # build report on income groups
  by_income = (
    pd.concat(
      [ ( dfs["normal"] .
          rename( columns = {"vat paid: mean":"normal"} ) ),
        ( dfs["holiday"] .
          rename( columns = {"vat paid: mean":"holiday"} ) ) ],
      axis = "columns" ) )
  def add_estimate( can_shift_by : int,
                    name : str ):
    """ Assuming rationality, if people can shift their purchase times
    by a month, then effectively the VAT holiday is two months,
    regardless of how long it is by law. """
    by_income["spent " + name] = (1/365) * (
      (365 - 2 * can_shift_by) * dfs["normal"] +
             2 * can_shift_by  * dfs["holiday"]  )
    by_income["saved " + name] = (
      by_income["normal"] - by_income["spent " + name] )
    by_income["saved % " + name] = 100 * (
      by_income["saved " + name] /  by_income["normal"] )
  shift_windows = [
    ( 1.5, "no shift" ),
    ( 15, "15 days" ),
    ( 30, "30 days" ),
    ( 90, "90 days" ),
    ( 182.5, "permanent" ) ]
  for (r,n) in shift_windows: add_estimate(r,n)
  by_income

if True: # build federal VAT income report
  vat_revenue = inflator * 59917589707522
    # Before inflation, this figure is VAT revenue in 2017,
    # which was about 6e13 before inflation.
  federal = ( by_income.loc["all"] *
              vat_revenue / by_income.loc["all","normal"] )
  for (_,n) in shift_windows:
    federal["saved % " + n] = ( # Unlike peso values,
                            # percentages should not be scaled
      by_income.loc[ "all", "saved % " + n] )
  federal
