import numpy as np
import pandas as pd


def read_sizes (path,filename):
  files = {}
  for i in [1,10,100,1000]:
    files[i] = pd.read_csv(
      path + "recip-" + str(i) + "/" + filename + ".csv" )
  return files


if True: # read data
  path = "output/vat-data/"
  # purchases = read_sizes( "1.purchases" )              # pitfall: memory hog
  ppt =   read_sizes( path, "2.purchases,prices,taxes" ) # pitfall: memory hog
  ple =   read_sizes( path, "3.person-level-expenditures" )
  demog = read_sizes( path, "4.demog" )
  final =   read_sizes( path, "5.final" )
  del(path)


##
# Why no vat for so many?
##

final_novat = final [1] [ final [1] ["vat-paid"] <= 0
                    ]

if True: # show some things
  final [1] . describe().round(2)
  final_novat.describe().round(2)
  final_novat[["household","household-member","transactions"]].iloc[0:5]

if True: # Check out the first (household,member) pair in final_novat with transactions > 15
  house1 = 100008
  mbr1 = 1
  ppt1 = ppt[1]
  ppt1 [ (ppt1["household"] == house1) & (ppt1["household-member"] == 1) ]
  del(mbr1,house1)
  # It looks legit. The "problem" is that the VAT is zero for lots of goods; see some-vat-exemptions.txt


##
# Cross sections
##

