# PITFALL: In this file, the 3rd command-line argument means something different,
# and there is a fourth. They are still parsed by the `common` library.

import pandas as pd
import numpy as np

import python.build.output_io as oio
import python.build.common as common


if      common.del_rosario_exemption_source == 'auto':
  exemptions = pd.read_csv( "output/vat/tables/recip-" + str(common.subsample)
                          + "/goods,first_six_deciles.csv" )
elif common.del_rosario_exemption_source == 'manual':
  exemptions = pd.read_csv( "data/vat/exemptions"
                          + "/goods,first_six_deciles.csv" )

exemptions = exemptions.head( common.del_rosario_exemption_count )


## the rest is tests

print( exemptions )
