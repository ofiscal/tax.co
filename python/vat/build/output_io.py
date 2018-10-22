import pandas as pd
import os


def saveStage(subsample,data,name):
  path = 'output/vat/data/recip-' + str(subsample)
  if not os.path.exists(path): os.makedirs(path)
  data.to_csv( path + '/' + name + ".csv"
             , index = False )

def readStage(subsample,name,**kwargs):
  path = 'output/vat/data/recip-' + str(subsample)
  return pd.read_csv( path + '/' + name + ".csv"
                    , **kwargs )
