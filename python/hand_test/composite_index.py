# This creates a single key from a collection of keys,
# so that a dataset can be compared to a previous one using csv-diff, e.g.:
#   csv-diff old.csv new.csv --key="id"

if True:
  import sys
  import pandas                    as pd
  #
  import python.build.output_io    as oio
  import python.common.common      as cl

p4 = oio.readStage( cl.subsample
                   , "people_3_income_taxish." + cl.strategy_year_suffix )

p4["id"] = ( p4["household"]       .astype(str) + ":" +
             p4["household-member"].astype(str) )

p4.to_csv("old.csv")
