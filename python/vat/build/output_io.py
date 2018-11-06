import pandas as pd
import os


def saveStage(subsample,data,name,index=False):
  folder = 'output/vat/data/recip-' + str( subsample )
  if not os.path.exists( folder ):
    os.makedirs( folder )
  path = folder + '/' + name + ".csv"
  data.to_csv( path, index = index )

def readStage(subsample,name,**kwargs):
  path = 'output/vat/data/recip-' + str( subsample )
  return pd.read_csv( path + '/' + name + ".csv"
                    , **kwargs )
