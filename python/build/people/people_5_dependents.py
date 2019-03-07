import sys
import pandas as pd
import numpy as np

import python.util as util
import python.build.output_io as oio
import python.common.misc as c
import python.common.cl_fake as cl


ppl = oio.readStage( cl.subsample
                   , "people_4_ss." + cl.vat_strategy_suffix )

hh = ( ppl[["household","dependent"]]
       . groupby( "household" )
       . agg( 'sum' )
       . rename( columns = {"dependent":"dependents"} )
       . reset_index() )

ppl = ( ppl.merge( hh, how='inner', on='household' )
        . drop( columns = "dependent" ) )

ppl["has dependent"] = (
  ppl["member-by-income"] <= ppl["dependents"] )
