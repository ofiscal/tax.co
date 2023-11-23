# exec ( open ( "python/temp.py" ) . read () )

import os
import pandas as pd


if True: # Read and format the data
  raw_enph_folder = "data/enph-2017/3_csv/"

  ppl_dict = {
    "DIRECTORIO" : "household",
    "ORDEN"      : "member",
  }

  hh_dict = {
    "DIRECTORIO" : "household" ,
    "FEX_C"      : "weight" ,
    "IT"         : "IT",
    "GTUG"       : "GT",
  }

  ppl = ( # people
    pd.read_csv (
      os.path.join ( raw_enph_folder,
                     "Caracteristicas_generales_personas.csv" ),
      usecols = ppl_dict.keys () )
    . rename ( columns = ppl_dict ) )

  hhs = (
    pd.read_csv (
      os.path.join ( raw_enph_folder,
                     "Viviendas_y_hogares.csv" ),
      usecols = hh_dict . keys() )
    . rename ( columns = hh_dict ) )

  # Only hhs needs reformatting.
  for colname in ["weight","IT","GT"]:
    hhs[colname] = ( hhs[colname]
                     . str.replace ( ",", "." )
                     . astype (float) )

# Compute number of members, merge into households,
# and use to compute "IT/members" (income per capita)
if True:
  ppl_agg = (
    ppl.groupby ( "household" )
    . agg ("max")
    . reset_index ()
    . rename ( columns = {"member" : "members"} )
  )

  m = hhs.merge ( ppl_agg,
                  how = "left",
                  on = "household" )

  m["IT/members"] = m["IT"] / m["members"]

if True: # Define and examine deciles.
  m["decile"] = pd.qcut ( m["IT"],
                          10,
                          labels = False )

acc = []
for i in range(10):
  decile = m[ m["decile"] == i ]
  it_weighted_sum = decile["IT"] . sum()
  gt_weighted_sum = decile["GT"] . sum()
  acc.append (
    pd.DataFrame ( {
      "Decile"                : [ i],
      "Sum of IT"             : [ it_weighted_sum],
      "Sum of GT"             : [ gt_weighted_sum],
      "Sum of GT / Sum of IT" : [ gt_weighted_sum /
                                  it_weighted_sum]
    } ) )

pd.concat( acc )

# Result:
#
# Decile   Sum of IT     Sum of GT     Sum of GT / Sum of IT
#      0   2.672727e+09  6.721673e+09  2.514912
#      1   5.477734e+09  7.696810e+09  1.405108
#      2   8.059080e+09  9.705304e+09  1.204269
#      3   9.496003e+09  1.026278e+10  1.080747
#      4   1.211099e+10  1.208627e+10  0.997959
#      5   1.483465e+10  1.353978e+10  0.912713
#      6   1.829672e+10  1.555565e+10  0.850188
#      7   2.332340e+10  1.854458e+10  0.795106
#      8   3.212062e+10  2.271873e+10  0.707294
#      9   7.259432e+10  4.076627e+10  0.561563
