if True:
  import os
  import pandas                 as pd
  #
  import python.build.output_io as oio
  import python.common.common   as c
  import python.common.misc     as misc
  import python.common.terms    as t


consumables_by_coicop_prefix = (
  pd.read_csv (
    os.path.join ( "users",
                   c . user,
                   "config/vat/consumable_groups_by_coicop_prefix.csv" ) ) )

consumables_other = (
  pd.read_csv (
    os.path.join ( "users",
                   c . user,
                   "config/vat/consumable_groups_other.csv" ) ) )

if True: # Fill in any groups missing fromo consumables_other.
         # (Necessary because by default in the UI none of the radio buttons
         # are checked for the other consumables groups.)
  consumables_other_blank = (
    pd.read_csv ( "config/vat/grouped/consumable_groups_other.csv" )
    . rename ( columns = { "consumable group" : "group",
                           "rate group" : "vat" } ) )
  consumables_other_blank["vat"] = 0
  consumables_other = (
    pd.concat ( [ consumables_other,
                  consumables_other_blank ] )
    . groupby ( "group" )
    . agg ( "first" )
    . reset_index() )
  del(consumables_other_blank)

vat_cap_c = (
    misc . read_csv_or_xlsx (
        os.path.join (
          "config/vat/grouped/vat_by_capitulo_c" ),
        encoding = "utf-8" )
    . rename (
        columns = { "CODE" : "25-broad-categs"
                  , "DESCRIPTION" : "description" }
    ) )

vat_coicop = (
    misc . read_csv_or_xlsx (
        os.path.join (
          "config/vat/grouped/vat_by_coicop" ),
        encoding = "utf-8" ) )

vat_coicop = vat_coicop.drop (
  columns = ["prefix vat", "vat", "vat, min", "vat, max"] )
vat_coicop = vat_coicop.merge (
  consumables_by_coicop_prefix,
  left_on = "prefix",
  right_on = "group" )
vat_coicop_orig = vat_coicop.copy()

for g in consumables_other["group"]:
  v = ( consumables_other.loc
        [ consumables_other["group"] == g,
          "vat" ]
        . iloc[0] # Converts a single-valued series to a number.
        )
  vat_coicop[g] = vat_coicop[g] * v

vat_coicop.to_csv( "multiplied.csv" )
vat_coicop_orig.to_csv( "orig.csv" )

### VIEW

for i in vat_cap_c                    . columns : print(i)
for i in vat_coicop                   . columns : print(i)
for i in consumables_by_coicop_prefix . columns : print(i)
for i in consumables_other            . columns : print(i)
