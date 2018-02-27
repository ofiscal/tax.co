# The value-added tax.

import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles

taxRates = pd.DataFrame( { 'coicop' : range(1,1500)
                   , 'taxRate' : 0.19 } )
taxRates.loc[taxRates['coicop'] < 500, 'taxRate'] = 0.05

data = pd.read_csv(
  datafiles.folder(2017) + "recip-100/" + "st2_sea_enc_gcfhr_csv" + '.csv')
legend = { "nh_cgprcfh_p1"   : "good-in-words"
         , "nh_cgprcfh_p1s1" : "coicop"
         , "nh_cgprcfh_p2"   : "quantity"
         , "nh_cgprcfh_p3"   : "purchased=1"
         , "nh_cgprcfh_p4"   : "where-bought"
         , "nh_cgprcfh_p5"   : "value"
         , "nh_cgprcfh_p6"   : "frequency-bought"
         , "nh_cgprcfh_p7"   : "household-communal"
         }
data = data[ list(legend.keys()) ]
data=data.rename(columns=legend)
