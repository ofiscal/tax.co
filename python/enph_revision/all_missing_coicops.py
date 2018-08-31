# exec( open("python/enph_revision/all_missing_coicops.py").read() )

import pandas as pd
import numpy as np
import os


exec( open("python/enph_revision/coicop_data/load.py").read() )
exec( open("python/enph_revision/coicop_data/clean_and_join.py").read() )

coicop_data["count"] = 1
coicop_data["verbal"] = coicop_data["verbal"].fillna( "" )
coicop_data["verbal"] = coicop_data["verbal"].apply(str)
coicop_data["coicop"] = ( coicop_data["coicop"]
                          .fillna( "" )
                          .replace(" ", "") )
coicop_data["coicop"] = coicop_data["coicop"].apply(str).str.pad(8,"left","0")
coicop_vat[ "coicop"] = coicop_vat ["coicop"].apply(str).str.pad(8,"left","0")
grouped = (coicop_data
           .groupby( ["coicop","verbal","file"] )
           .sum()
           .reset_index()
           .sort_values(by=["coicop","file","verbal"])
           )

bridge_codes = list( coicop_vat["coicop"].unique() )
enph_codes   = list( grouped   ["coicop"].unique() )
unrecognized = set(enph_codes) - set(bridge_codes)

results = grouped[ grouped["coicop"].isin( unrecognized ) ]

# results.to_csv( "output/enph_revision/x.csv" )

result_string = (results . to_string(index=False) . split("\n") )

def first_word( string ): return string.split()[0]

# Stick a newline after every group of rows with the same COICOP.
def make_readable(previous_coicop, ls):
  if not ls: return []
  else:
    fw = first_word( ls[0] )
    if previous_coicop == fw: return [ls[0]] + f( fw, ls[1:] )
    else: return ["\n"] + [ls[0]] + f( fw, ls[1:] )

text_file = open("output/enph_revision/missing_coicops_with_context.csv", "w")
text_file.write(
  "\n".join(
    make_readable(
      "anabolic unicorn soldier mildew farm" # because this definitely won't be the first COICOP
      , result_string
    )
  )
)
text_file.close()
