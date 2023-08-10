# PURPOSE:
# Assign a 2-digit COICOP prefix to each of the Capitulo C categories.
#
# Just as the goods in the COICOP table have been assigned
# a 2-digit COICOP prefix
# (theoretically from 01 to 14, but in our data only from 01 to 12),
# so too must the Capitulo C data be assigned a 2-digit COICOP prefix.
#
# PITFALL:
# The Capitulo C table (at `paths.file_vat_cap_c_raw`)
# contains two COICOP columns, "coicop" and "coicop2".
# I believe that's because it wasn't obvious how to COICOP-classify
# each Capitulo C category.
# However, fortunately, they all have the same 2-digit COICOP prefix,
# which is all we need.

if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.grouped_vat.paths as paths


grouped = pd.read_csv (
  paths.file_vat_cap_c_raw,
  sep = "\t" )


###
### Create the "prefix" column.
###

grouped["coicop2"] = (
  # Where coicop2 is undefined, make it equal to coicop.
  grouped.apply (
    lambda row: (
                      row["coicop"]
      if   np.isnan ( row["coicop2"] )
      else            row["coicop2"]  ),
    axis = "columns" )
  . astype(int) )

# Compute the 2-digit prefix of each coicop code.
grouped = grouped.rename (
  columns = { "coicop" : "coicop1" } )
for i in ["1","2"]:
  grouped["coicop" + i] = util.pad_column_as_int (
    8, grouped ["coicop"+i] )
  grouped["prefix" + i] = grouped ["coicop"+i].str [:2]

# If the two prefixes agree (they do), call that the prefix.
grouped["prefix"] = (
  grouped.apply (
    ( lambda row:
         row["prefix1"]
      if row["prefix1"] == row["prefix2"]
      else np.nan ),
    axis = "columns" )
  . astype ( int ) )


### Replace VAT with the average of vat min and vat max.
### (In the original data it's not defined for all COICOP codes,
### and we don't actually use it.)
grouped["vat"] = ( grouped["vat, min"] + grouped["vat, max"] ) / 2

grouped = grouped.drop (
  columns = [ 'big categorie',
              'coicop1',
              'coicop2',
              'prefix1',
              'prefix2', ] )

grouped . to_csv ( paths.file_vat_cap_c,
                   index = False )
