if True:
  import pandas as pd
  import numpy as np
  import re # regex
  #
  import python.common.util as util


grouped = pd.read_csv (
  "config/vat/grouped/1.dos2unix/vat-by-coicop.tsv",
  sep = "\t" )

old = ( pd.read_csv (
  "config/vat/vat_by_coicop.csv" )
  [[ "coicop", "vat", "vat, min", "vat, max" ]] )


###
### Fix column names.
###

for i in grouped.columns: print(i)

fails = "pd.rename fails to change the name of this column, which is why I use regexes later."

grouped = grouped.rename (
  columns = {
    "Estupefacientes"              : "estupefacientes",
    "Para hombres"                 : "para hombres",
    "medicamentos (medicina)"      : "medicamentos",
    "impuestos saludables (bienes" : "impuestos saludables",
    "Categoría de productos por conexión (infantiles*)" : "infantiles",
    "De uso exclusivo para mujeres - personas con vulva/útero" : fails,
    "Rol de género  - femenino"                                : fails,
  } )

grouped = grouped.rename (
  columns = lambda x: re.sub (
    ".*exclusivo para mujeres.*", "used only by females", x ) )

grouped = grouped.rename (
  columns = lambda x: re.sub (
    ".*Rol de g.*fem.*", "female gender role", x ) )


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

# Use the old VAT values.
grouped = grouped.drop ( columns = ["vat","vat, min", "vat, max"] )
grouped = grouped.merge ( old, on = "coicop" )

# Replace VAT with the average of vat min and vat max.
# (In the original data it's not defined for all COICOP codes,
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

grouped.to_csv ( "config/vat/grouped/vat_by_coicop.csv" )
