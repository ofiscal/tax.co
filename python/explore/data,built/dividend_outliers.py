# Running it is the easiest way to see what this does.
# It shows dividend income for the top five dividend-earning households in each income percentile.
# Upshot: Dividend earnings averages for each percentile are driven by a few extreme observations.
# (Each percentile has 872 members.)

import sys
import numpy as np
import pandas as pd
import re as regex


h_all = pd.read_csv( "output/vat/data/recip-1/" + "households.detail_.csv" )
h = pd.read_csv( "output/vat/data/recip-1/" + "households.detail_.csv"
               , usecols = ["household", "income-percentile", "income", "income, dividend"]
               )

gs = h.groupby( "income-percentile" )

for i in range(0,100):
  g = gs . get_group(i)
  print( "\npercentile: " + str(i) )
  print( "mean income: " + format( "%e" % g["income"].mean() ) )
  print( "mean dividend income: " + format( "%e" % g["income, dividend"].mean() ) )
  print( "top five dividend-earning households: " )
  print( g . sort_values( "income, dividend"
                        , ascending=False )
         [0:5] )
