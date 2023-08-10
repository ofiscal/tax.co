if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.grouped_vat.paths as paths


grouped = pd.read_csv (
  paths.file_vat_coicop_raw,
  sep = "\t" )

old = ( pd.read_csv (
  "config/vat/vat_by_coicop.csv" )
  [[ "coicop", "vat", "vat, min", "vat, max" ]] )


###
### Add 2-digit COICOP prefix column
###

grouped["coicop"] = util.pad_column_as_int (
  8, grouped["coicop"] )  # Now COICOP is a string.
grouped["prefix"] = (     # Create the prefix.
  grouped["coicop"]
  . apply( lambda s: int ( s[:2] ) ) )
grouped["coicop"] = ( # Turn COICOP back to an int.
  grouped ["coicop"]
  . apply ( lambda x: int(x) ) )


###
### Massage the VAT variables.
###

# Use the old VAT values of ["vat","vat, min", "vat, max"]
# (and leave everything else unchanged).
grouped = grouped.drop ( columns = ["vat","vat, min", "vat, max"] )
grouped = grouped.merge ( old, on = "coicop" )

# Replace VAT with the average of vat min and vat max.
# (In the original data, "vat" is's not defined for all COICOP codes,
# and we don't actually use it.)
grouped["vat"] = ( grouped["vat, min"] + grouped["vat, max"] ) / 2

# Approximate each prefix group's VAT rate to the set [0,0.05,0.19].
prefixes = (
  grouped [["prefix","vat"]]
  . groupby ( "prefix" )
  . agg ( "mean" )
  . rename ( columns = { "vat" : "prefix mean vat" } )
  . reset_index() )
prefixes["prefix vat"] = (
  prefixes["prefix mean vat"]
  . apply ( lambda cell:
            ( 0 if cell < 0.025
              else ( 0.05 if cell < ( ( 0.05 + 0.19 ) / 2 )
                     else 0.19 ) ) ) )
grouped = ( grouped
            . merge ( prefixes, on = "prefix" )
            . drop ( columns = ["prefix mean vat"] ) )


###
### Visual checks
###

grouped . describe () . transpose ()
p = grouped[["coicop","prefix","vat","prefix vat"]]
p[ p["prefix"]==7 ].describe()
p[ p["prefix"]==10 ].describe()


###
### Write
###

grouped.to_csv ( paths.file_vat_coicop,
                 index = False )
