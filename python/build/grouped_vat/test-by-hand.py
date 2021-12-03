if True:
  import pandas as pd
  import numpy as np
  import os


###
### Maybe a different paradigm; was a separate file.
###

folder = "config/vat/grouped/"
coicop_path = os.path.join ( folder, "vat_by_coicop.csv" )
cap_c_path  = os.path.join ( folder, "vat_by_capitulo_c.csv" )
coicop = pd.read_csv ( coicop_path )
cap_c  = pd.read_csv ( cap_c_path )
coi_names = set ( coicop.columns )
cap_names = set ( cap_c.columns )

print ( coi_names - cap_names )
print ( cap_names - coi_names )

del ( folder,
      coicop_path, cap_c_path,
      coicop,      cap_c,
      coi_names,   cap_names )

###
### Maybe a different paradigm; was a separate file.
###

if True: # Get the data
  # The old data
  coicop   = pd.read_csv ( "config/vat/vat_by_coicop.csv" )
  cap_c    = pd.read_csv ( "config/vat/vat_by_capitulo_c.csv" )
  #
  # The new data, with groups
  g_coicop = pd.read_csv ( "config/vat/grouped/vat_by_coicop.csv" )
  g_cap_c  = pd.read_csv ( "config/vat/grouped/vat_by_capitulo_c.csv" )

vat_columns = ["vat", "vat, min", "vat, max"]
#
comparing_on = ["coicop"] + vat_columns
assert coicop [comparing_on ] . equals (
  g_coicop [ comparing_on ] )
#
comparing_on = ["CODE"] + vat_columns
assert cap_c [comparing_on ] . equals (
  g_cap_c [ comparing_on ] )

comparing_on = ["coicop"] + vat_columns
cc = pd.concat ( [coicop   [vat_columns],
                  g_coicop [vat_columns]],
                 axis = "columns" )

(coicop["coicop"]   == g_coicop["coicop"] )   .all()
(coicop["vat, min"] == g_coicop["vat, min"] ) .all()
(coicop["vat, max"] == g_coicop["vat, max"] ) .all()

min_is_max = coicop["vat, min"] == coicop["vat, max"]
(coicop[min_is_max]["vat"] == g_coicop[min_is_max]["vat"] )


cc [ ~ coicop [comparing_on ].eq (
     g_coicop [ comparing_on ] ) ]

cc [ coicop["vat"] != g_coicop["vat"] ]

assert coicop [comparing_on ] . equals (
  g_coicop [ comparing_on ] )
