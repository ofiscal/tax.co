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
                   "config/vat/consumable_groups_by_coicop_prefix.csv" ) )
  . rename ( columns = { "vat" : "prefix vat" } ) )

consumables_other = (
  pd.read_csv (
    os.path.join ( "users",
                   c . user,
                   "config/vat/consumable_groups_other.csv" ) ) )

if True: # In consumables_other, fill in any missing groups.
         # (This is Necessary because by default in the UI none of the
         # radio buttons are checked for the other consumables groups.)
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
        encoding = "utf-8" )
  . drop ( columns = ["prefix vat"] )
  . rename ( columns = {"DESCRIPTION" : "description" } ) )

def incorporate_user_vat_prefs ( data : pd.DataFrame
                               ) -> pd.DataFrame:
  # PURPOSE: Merge user's VAT preferences into vat_coicopg and vat_cap_c.
  # PITFALL: This function is impure, as it depends on the runtime values
  # of `consumables_by_coicop_prefix` and `consumables_other`.
  # TODO: Test (automatically).
  data = ( data
    . drop ( columns = ["vat", "vat, min", "vat, max"] )
    . rename ( columns = { "prefix" : "group" } )
    . merge ( consumables_by_coicop_prefix,
              on = "group" ) )
  for g in consumables_other["group"]:
    v = ( consumables_other.loc
          [ consumables_other["group"] == g,
            "vat" ]
          . iloc[0] # Converts a single-valued series to a number.
          )
    data[g] = data[g] * v
  return data

vat_components = ( list ( consumables_other ["group"] )
                   + ["prefix vat"] )

def compute_total_vat ( data : pd.DataFrame
                      ) -> pd.DataFrame:
  # Sum the prefix vat and the rates for the other consumable groups.
  # Also compute "vat frac" = vat / (1 + vat).
  # TODO: Test (automatically).
  data["vat"] = ( data [ vat_components ]
                  . sum ( axis = "columns" ) )
  data["vat frac"] = (  data ["vat"] /
                       (data ["vat"] + 1) )
  return data

def go ( data : pd.DataFrame
       ) -> pd.DataFrame:
  return (
    compute_total_vat (
      incorporate_user_vat_prefs ( data ) )
    . drop ( # Once they have been summed, the components are of no interest.
      columns = vat_components + ["group"] ) )

vat_coicop = go ( vat_coicop )
vat_cap_c  = go ( vat_cap_c )

if True: # save
  oio.saveStage ( c.subsample
                , vat_coicop
                , 'vat_coicop.' + c.strategy_suffix )
  oio.saveStage ( c.subsample
                , vat_cap_c
                , 'vat_cap_c.'  + c.strategy_suffix )
  #
  vat_coicop = vat_coicop.drop( columns = ["description","Notes"] )
  vat_cap_c  = vat_cap_c .drop( columns = ["description"        ] )
  #
  oio.saveStage ( c.subsample
                , vat_coicop
                , 'vat_coicop_brief.' + c.strategy_suffix )
  oio.saveStage ( c.subsample
                , vat_cap_c
                , 'vat_cap_c_brief.'   + c.strategy_suffix )
