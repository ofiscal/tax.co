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

  # Only `hhs` needs reformatting.
  for colname in ["weight","IT","GT"]:
    hhs[colname] = ( hhs[colname]
                     . str.replace ( ",", "." )
                     . astype (float) )

# Compute number of members, merge into households,
# and use to compute "IT-per-capita" (income per capita)
if True:
  ppl_agg = ( # Find number of members in each household.
    ppl.groupby ( "household" )
    . agg ("max")
    . reset_index ()
    . rename ( columns = {"member" : "members"} )
  )

  m = hhs.merge ( ppl_agg,
                  how = "left",
                  on = "household" )

  m["IT-per-capita"] = (
    m["IT"] / m["members"] )

if True: # Compute weighted deciles (janky!)
  tenth_weight = m["weight"].sum() / 10

  if True: # First, define a weighted decile for "IT"
    decile_defining_var = "IT"
    m = m . sort_values ( decile_defining_var )
    last_index = 7284 # I found this by hand, if sorting on IT
    assert m.iloc[:last_index + 1]["weight"].sum() >= tenth_weight
    assert m.iloc[:last_index]    ["weight"].sum() <  tenth_weight

    weighted_lowest_decile_sorted_on_it = (
      # The lowest decile is the first `n` poorest households,
      # such that the sum of their weights is one tenth of the total.
      m . iloc[:last_index] . copy() )

  if True: # Do it again for "IT-per-capita"
    decile_defining_var = "IT-per-capita"
    m = m . sort_values ( decile_defining_var )
    last_index = 7224 # I found this by hand, if sorting on IT-per-capita
    ratio = m.iloc[:last_index] ["weight"].sum() / tenth_weight
    assert (ratio > 0.99) & (ratio < 1.01) # The last index is unstable, but near this.

    weighted_lowest_decile_sorted_on_it_over_members = (
      # The lowest decile is the first `n` poorest households,
      # such that the sum of their weights is one tenth of the total.
      m . iloc[:last_index] . copy() )

  # Define unweighted deciles.
  m["decile, unweighted"] = pd.qcut (
    m[ decile_defining_var ],
    10,
    labels = False )

def describe_deciles (
    decile_defining_var : str, # "IT" or "IT-per-capita"
    extra_weighted_decile : pd.DataFrame, # In addition to the unweighted deciles,
                                          # must can include a weighted one.
) -> pd.DataFrame:

  def describe_subset (
      # This will be used to describe deciles,
      # weighted or unweighted.
      subset_name : str,
      df0 : pd.DataFrame ) -> pd.DataFrame:
    df = df0.copy()
    n_households = len ( df["household"] . drop_duplicates() )
    assert len (df) == n_households # households are not repeated
    weight_sum = df ["weight"] . sum ()
    return pd.DataFrame ( {
      "Decile"              : [ subset_name                             ],
      "n households"        : [ n_households                            ],
      "Sum of weight"       : [   df["weight"]                  . sum() ],
      "Sum of IT"           : [   df["IT"    ]                  . sum() ],
      "Sum of GT"           : [   df["GT"    ]                  . sum() ],
      "Sum of IT, weighted" : [ ( df["IT"    ] * df["weight"] ) . sum() ],
      "Sum of GT, weighted" : [ ( df["GT"    ] * df["weight"] ) . sum() ],
    } )

  summaryList = [] # a list in which to accumulate descriptions of deciles
  summaryList.append (
    # Start by appending the weighted 0th decile.
    describe_subset ( subset_name = "weighted 0",
                      df0 = extra_weighted_decile ) )
  for i in range(10):
    # Then add all the unweighted deciles (including the 0th).
    decile = m[ m["decile, unweighted"] == i ]
    summaryList.append (
      describe_subset ( str(i),
                        decile )
    )

  summary : pd.DataFrame = (
    # Make a table out of those decile descriptions.
    pd.concat ( summaryList )
    . reset_index ( drop = True ) )

  # Compute a few more columns.
  summary[ "Sum of GT / n households" ]  = ( summary [ "Sum of GT" ] /
                                             summary [ "n households" ] )
  summary[ "Sum of IT / n households" ]  = ( summary [ "Sum of IT" ] /
                                             summary [ "n households" ] )
  summary[ "Sum of GT / Sum of weight" ] = ( summary [ "Sum of GT" ] /
                                             summary [ "Sum of weight" ] )
  summary[ "Sum of IT / Sum of weight" ] = ( summary [ "Sum of IT" ] /
                                             summary [ "Sum of weight" ] )
  summary[ "Sum of GT / Sum of IT" ]     = ( summary [ "Sum of GT" ] /
                                             summary [ "Sum of IT" ] )
  summary[ "Wsum of GT / Wsum of IT" ]   = ( summary [ "Sum of GT, weighted" ] /
                                             summary [ "Sum of IT, weighted" ] )
  return summary

for ( decile_defining_var, extra_weighted_decile ) in [
    ( "IT",            weighted_lowest_decile_sorted_on_it),
    ( "IT-per-capita", weighted_lowest_decile_sorted_on_it_over_members) ]:
  df = describe_deciles ( decile_defining_var = decile_defining_var,
                          extra_weighted_decile = extra_weighted_decile )
  print ( decile_defining_var )
  print ( df )
  df.to_csv (
    "." . join ( [
      "IT-and-GT-by-household-decile",
      "sorting-on-" + decile_defining_var,
      ".csv" ] ),
    index = False,
  )
