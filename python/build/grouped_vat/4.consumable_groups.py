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
               . sort_values ( "consumable group" )
                [[ "consumable group", "rate group" ]] )
  prefixes . to_csv (
    paths.file_consumable_groups_by_coicop,
    index = False )

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
  other_groups.to_csv ( paths.file_consumable_groups_other,
                        index = False )
