# exec( open("python/enph_revision/all_missing_coicops.py").read() )

import pandas as pd
import numpy as np
import os

subsample = 100
exec( open("python/enph_revision/coicop_data/load.py").read() )
exec( open("python/enph_revision/coicop_data/clean_and_join.py").read() )

coicop_data["count"] = 1
coicop_data["verbal"] = coicop_data["verbal"].fillna( "absent" )
coicop_data["verbal"] = coicop_data["verbal"].apply(str)
coicop_data["coicop"] = coicop_data["coicop"].fillna( "absent" )
coicop_data["coicop"] = coicop_data["coicop"].apply(str)
results = coicop_data.groupby( ["coicop","verbal","file"] ).sum().reset_index().sort_values(by=["coicop","file","verbal"])
results.to_csv("output/enph_revision/missing_coicops.csv")

# TODO NEXT: Remove overlap from our COICOP key (ala coicop_search.py).
