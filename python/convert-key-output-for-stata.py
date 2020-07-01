if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.common as com
  import python.build.output_io as oio


subsample = 1
source = "output/vat/data/recip-" + str(subsample) + "/"
dest   = "output-as-stata/recip-" + str(subsample) + "/"

# if True: # purchases
#   df = pd.read_csv( source + "purchases_2_vat.detail.csv" )
#   df.to_stata( dest + "purhcases.dta" )

if True: # people
  df = pd.read_csv( source + "people_4_income_taxish.detail.2018.csv" )
  df.to_stata( dest + "people.dta" )

if True: # households
  df = pd.read_csv( source + "households_2_purchases.detail.2018.csv" )
  df.describe().transpose()[["count","min","max"]]
  df.replace( np.inf, np.nan, inplace = True )
  df.describe().transpose()[["min","max"]]
  df.to_stata( dest + "households.dta" )

