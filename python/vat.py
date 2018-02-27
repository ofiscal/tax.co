# The value-added tax.

import numpy as np
import pandas as pd
import python.util as util

taxRates = pd.DataFrame( { 'coicop' : range(1,1500)
                   , 'taxRate' : 0.19 } )
taxRates.loc[taxRates['coicop'] < 500, 'taxRate'] = 0.05

