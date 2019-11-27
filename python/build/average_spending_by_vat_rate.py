if True:
  import sys
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.output_io as oio
  from python.build.people.files import edu_key
  import python.common.common as c
  #
  if c.regime_year == 2016:
    import python.regime.r2016 as regime
  else: import python.regime.r2018 as regime


households = oio.readStage(
  c.subsample,
  "households." + c.strategy_year_suffix )

households["value, normal vat"] = (
  households["value, vat 0"] +
  households["value, vat 5"] +
  households["value, vat 19"] )

def sci(number):
  return "{:.2e}".format(number)

def pct(number):
  return "{:.2%}".format(number)

if True:
  print("=====================")
  print( "Across-household average spending subject to:" )
  for i in [0,5,19]:
    print( str(i) + " VAT:",
           sci(
             households["value, vat " + str(i)].mean() ) )
  print( "Note that the above omits a small fraction of spending,",
         "as the effective tax rate on a good can be something else." )
  for (total_col, explainer) in [
      ("value"             , "Including"),
      ("value, normal vat" , "Excluding") ]:
    print()
    print(explainer + " goods with an effective tax rate other than 0, 5 or 19% in total spending")
    print("=====================")
    #
    print( "Average household spending: "
           + sci( households[total_col].mean() ) )
    print( "Across-household average fraction of spending subject to:" )
    for i in [0,5,19]:
      print( str(i) + "% VAT:",
             pct(
               ( households["value, vat " + str(i)]
                 / households[total_col] )
               .mean() ) )

