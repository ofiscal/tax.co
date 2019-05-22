import pandas as pd
import os


def test_clear( filename ):
  f = "output/test/" + filename + ".txt"
  if os.path.exists( f ): os.remove( f )

def test_write( filename, content ):
  with open("output/test/" + filename + ".txt" ,'a+') as f:
        f.write( " ".join( map( str, content ) )
               + "\n" )

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
