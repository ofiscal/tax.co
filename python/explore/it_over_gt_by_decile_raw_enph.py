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

accList = []
for i in range(10):
  decile = m[ m["decile"] == i ]
  accList.append (
    pd.DataFrame ( {
      "Decile"              : [ i],
      "Sum of IT"           : [   decile["IT"] . sum() ],
      "Sum of GT"           : [   decile["GT"] . sum() ],
      "Sum of IT, weighted" : [ ( decile["IT"] * decile["weight"] ) . sum() ],
      "Sum of GT, weighted" : [ ( decile["GT"] * decile["weight"] ) . sum() ],
    } ) )

acc = ( pd.concat ( accList )
        . reset_index ( drop = True ) )

acc[ "Sum of GT / Sum of IT" ] = ( acc [ "Sum of GT" ] /
                                   acc [ "Sum of IT" ] )
acc[ "Ws of GT / Wsum of IT" ] = ( acc [ "Sum of GT, weighted" ] /
                                   acc [ "Sum of IT, weighted" ] )

acc

# Results
#
#  Decile     Sum of IT     Sum of GT  Sum of IT, weighted  Sum of GT, weighted  Sum of GT / Sum of IT  Ws of GT / Wsum of IT
#       0  2.672727e+09  6.721673e+09         5.368087e+11         1.198133e+12               2.514912               2.231955
#       1  5.477734e+09  7.696810e+09         1.025721e+12         1.394381e+12               1.405108               1.359416
#       2  8.059080e+09  9.705304e+09         1.340730e+12         1.605673e+12               1.204269               1.197611
#       3  9.496003e+09  1.026278e+10         1.632191e+12         1.767233e+12               1.080747               1.082736
#       4  1.211099e+10  1.208627e+10         1.898405e+12         1.944570e+12               0.997959               1.024317
#       5  1.483465e+10  1.353978e+10         2.304079e+12         2.144411e+12               0.912713               0.930702
#       6  1.829672e+10  1.555565e+10         2.824643e+12         2.498798e+12               0.850188               0.884642
#       7  2.332340e+10  1.854458e+10         3.436916e+12         2.920132e+12               0.795106               0.849637
#       8  3.212062e+10  2.271873e+10         4.782152e+12         3.663942e+12               0.707294               0.766170
#       9  7.259432e+10  4.076627e+10         1.251539e+13         8.259613e+12               0.561563               0.659957
