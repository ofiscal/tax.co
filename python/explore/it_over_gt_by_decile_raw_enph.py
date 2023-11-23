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


if True: # Define and examine deciles, most of them unweighted.

  decile_defining_var = "IT/members" # "IT" and "IT/members" are both interesting

  if True: # Computing the jankiest weighted lowest decile.
    tenth_weight = m["weight"].sum() / 10
    last_index = 7525 # I found this by hand.
    assert m.iloc[:last_index + 1]["weight"].sum() >= tenth_weight
    assert m.iloc[:last_index]    ["weight"].sum() <  tenth_weight
    weighted_lowest_decile = ( m
                               . sort_values ( decile_defining_var )
                               . iloc[:last_index] )

  m["decile, unweighted"] = pd.qcut ( m[ decile_defining_var ],
                                      10,
                                      labels = False )

  def describe_subset ( subset_name : str,
                        df : pd.DataFrame ) -> pd.DataFrame:
    return pd.DataFrame ( {
      "Decile"              : [ subset_name ],
      "Sum of IT"           : [   df["IT"] . sum() ],
      "Sum of GT"           : [   df["GT"] . sum() ],
      "Sum of IT, weighted" : [ ( df["IT"] * df["weight"] ) . sum() ],
      "Sum of GT, weighted" : [ ( df["GT"] * df["weight"] ) . sum() ],
    } )

  accList = [] # a list in which to accrete descriptions of
  accList.append (
    describe_subset ( "weighted 0",
                      weighted_lowest_decile ) )
  for i in range(10):
    decile = m[ m["decile, unweighted"] == i ]
    accList.append (
      describe_subset ( str(i),
                        decile )
    )

  acc = ( pd.concat ( accList )
          . reset_index ( drop = True ) )

  acc[ "Sum of GT / Sum of IT" ] = ( acc [ "Sum of GT" ] /
                                     acc [ "Sum of IT" ] )
  acc[ "Wsum of GT / Wsum of IT" ] = ( acc [ "Sum of GT, weighted" ] /
                                       acc [ "Sum of IT, weighted" ] )


acc # The result


# Results, if decile_defining_var = "IT/members"
#
#      Decile     Sum of IT     Sum of GT  Sum of IT, weighted  Sum of GT, weighted  Sum of GT / Sum of IT  Wsum of GT / Wsum of IT
#  weighted 0  2.902086e+09  6.745345e+09         5.937897e+11         1.216732e+12               2.324309                 2.049096
#           0  3.768656e+09  7.978665e+09         7.587045e+11         1.441257e+12               2.117111                 1.899629
#           1  7.941213e+09  9.984152e+09         1.455360e+12         1.775537e+12               1.257258                 1.219999
#           2  9.542510e+09  1.038566e+10         1.574423e+12         1.737850e+12               1.088357                 1.103801
#           3  1.193796e+10  1.191160e+10         1.864963e+12         1.931906e+12               0.997792                 1.035895
#           4  1.400936e+10  1.293686e+10         2.155178e+12         2.043198e+12               0.923444                 0.948041
#           5  1.664439e+10  1.443002e+10         2.513932e+12         2.273739e+12               0.866960                 0.904455
#           6  1.877937e+10  1.549272e+10         3.017311e+12         2.593903e+12               0.824986                 0.859674
#           7  2.292190e+10  1.742693e+10         3.368491e+12         2.662958e+12               0.760274                 0.790549
#           8  3.005364e+10  2.131843e+10         4.347225e+12         3.311412e+12               0.709346                 0.761730
#           9  6.338725e+10  3.573281e+10         1.124145e+13         7.625127e+12               0.563722                 0.678305


# Results, if decile_defining_var = "IT"
#
#      Decile     Sum of IT     Sum of GT  Sum of IT, weighted  Sum of GT, weighted  Sum of GT / Sum of IT  Wsum of GT / Wsum of IT
#  weighted 0  1.935811e+09  5.474161e+09         3.952538e+11         9.717309e+11               2.827839                 2.458499
#           0  2.672727e+09  6.721673e+09         5.368087e+11         1.198133e+12               2.514912                 2.231955
#           1  5.477734e+09  7.696810e+09         1.025721e+12         1.394381e+12               1.405108                 1.359416
#           2  8.059080e+09  9.705304e+09         1.340730e+12         1.605673e+12               1.204269                 1.197611
#           3  9.496003e+09  1.026278e+10         1.632191e+12         1.767233e+12               1.080747                 1.082736
#           4  1.211099e+10  1.208627e+10         1.898405e+12         1.944570e+12               0.997959                 1.024317
#           5  1.483465e+10  1.353978e+10         2.304079e+12         2.144411e+12               0.912713                 0.930702
#           6  1.829672e+10  1.555565e+10         2.824643e+12         2.498798e+12               0.850188                 0.884642
#           7  2.332340e+10  1.854458e+10         3.436916e+12         2.920132e+12               0.795106                 0.849637
#           8  3.212062e+10  2.271873e+10         4.782152e+12         3.663942e+12               0.707294                 0.766170
#           9  7.259432e+10  4.076627e+10         1.251539e+13         8.259613e+12               0.561563                 0.659957
