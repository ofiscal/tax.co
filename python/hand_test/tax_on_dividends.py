# TODO automate these tests.

import sys
import pandas                    as pd

import python.build.ss_functions as ss
import python.build.output_io    as oio
import python.common.util               as util
import python.common.misc as c
import python.common.common as cl


### TODO : This duplicates a bit of code in python/build/people_3_income_taxish.py.
### Factor that out when automating tests.

ppl = pd.DataFrame( {"dividends": [i * c.uvt for i in [0,600,1000,1001]] } )

ppl["value, tax, purchaselike non-VAT"] = ppl["dividends"].apply(
  lambda x:
    0                                     if x < (600  * c.uvt)
    else (      (x - 600  * c.uvt) * 0.05 if x < (1000 * c.uvt)
           else (x - 1000 * c.uvt) * 0.1 + 20 * c.uvt ) )


### This isn't very informative, because almost nobody makes dividend income.

ppl = oio.readUserData( cl.subsample
  , 'people_3_income_taxish.' + cl.strategy_suffix)

pHigh = ppl[ ppl["income, dividend"] > 0 ]
pHigh[["tax on dividends","income, dividend"]]
