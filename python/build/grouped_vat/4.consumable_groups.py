if True:
  import pandas as pd
  import numpy as np
  import os
  import re # regex
  #
  import python.build.grouped_vat.paths as paths


if True: # input data
  vat_coicop  = pd.read_csv ( paths.file_vat_coicop )
  rate_groups = pd.read_csv ( "config/vat/rate_groups.csv" )

if True: # COICOP prefix groups
  prefixes = ( vat_coicop
               . groupby ( "prefix" )
               [["prefix vat"]]
               . agg ( "first" )
               . reset_index ()
               . rename ( columns =
                          {"prefix vat" : "rate"} )
               .  merge( rate_groups,
                         on = "rate" ) )
  prefixes = ( prefixes
               . rename ( columns = {"prefix" : "consumable group"} )
               . sort_values ( "consumable group" ) )
  prefixes["is prefix"] = True

if True: # Other groups of consumables, e.g. "pink tax"
  other_groups = (
    pd.DataFrame (
      { "consumable group" :
        list ( set ( vat_coicop.columns )
               - set ( [ "DESCRIPTION",
                         "coicop",
                         "Notes",
                         "prefix",
                         "vat",
                         "vat, min",
                         "vat, max",
                         "prefix vat",
                        ] ) ) } ) )
  other_groups["rate group"] = 0
  other_groups["is prefix"] = False

consumable_groups = pd.concat (
  [ prefixes     [[ "consumable group", "rate group", "is prefix" ]],
    other_groups [[ "consumable group", "rate group", "is prefix" ]] ],
  axis = "rows" )

consumable_groups.to_csv ( paths.file_consumable_groups,
                           index = False )
