# Write to .csv the summary statistics of a file.

import pandas as pd
import numpy as np

import python.common.common as cl
import python.build.output_io as oio


pcs = oio.readStage( cl.subsample
                    , "purchases_2_vat." + cl.strategy_suffix )

( util
  . describeWithMissing( pcs )
  . to_csv( "temp.csv") )
