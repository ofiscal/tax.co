# exec( open("python/enph_revision/all_missing_coicops.py").read() )

import pandas as pd
import numpy as np
import os

subsample = 100
exec( open("python/enph_revision/coicop_data/load.py").read() )
exec( open("python/enph_revision/coicop_data/clean_and_build.py").read() )

coicop_data["count"] = 1
coicop_data["verbal"] = coicop_data["verbal"].fillna( "" )
coicop_data["coicop"] = coicop_data["coicop"].fillna( -1 )
results = coicop_data.groupby( ["coicop","verbal"] ).sum().reset_index().sort_values(by="coicop")
results.to_csv("output/enph_revision/missing_coicops.csv")


# TODO NEXT: Delete inv* items from COICOP. convert " " to "-1".
# TODO NEXT: Remove overlap from our COICOP key (ala coicop_search.py).
