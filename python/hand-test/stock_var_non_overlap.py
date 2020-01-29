# What this is for
##################
# This demosntrates that indeed the two stock variables are non-overlapping,
# such that it is valid to compute an individual's stock income as their maximum.
#
# How to run it
###############
# Set the subsample size to 1 (everything) in cl_fake, and modify people.files
# to import cl_fake instead of cl_args.


import sys
import numpy as np
import pandas as pd
import re as regex

import python.common.misc as c
import python.common.common as cl
import python.build.people.files as files
import python.build.output_io as oio


ppl = c.all_columns_to_numbers(
  cl.collect_files( files.files
                  , subsample = cl.subsample )
  , skip_columns = ["non-beca sources"] # PITFALL : a space-separated list of ints
)

ppl = ppl.drop( # drop non-members of household
  ppl[ ppl["relationship"].isin( [6,7,8] )
  ].index )

if True: # remap some boolean integers
  for cn in ( [ "female" ] + # originally 1=male, 2=female
              [included for (quantity,included) in files.inclusion_pairs]
                             # originally 1=included, 2=forgot
  ): ppl[cn] = ppl[cn] - 1
  for cn in [ "student"         # originally 1=student, 2=not
            , "skipped 3 meals" # originally 1=yes, 2=no
            , "literate"        # originally 1=yes, 2=no
  ]: ppl[cn] = 2 - ppl[cn]

ppl["stock 1"] = ppl["income, year : sale : stock"]
ppl["stock 2"] = ppl["income, year : sale : stock ?2"]
ppl["stock max"] = ppl[["stock 1", "stock 2"]].max(axis=1)

stocks = ppl[ ppl["stock max"] > 0] [["stock 1", "stock 2", "stock max"]]
stocks
