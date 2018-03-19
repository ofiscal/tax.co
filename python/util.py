import pandas as pd
import math as math

def printInRed(message):
    """from https://stackoverflow.com/a/287934/916142"""
    CSI="\x1B["
    print( CSI+"31;40m" + message + CSI + "0m")

def describeWithMissing(df):
  x = df.describe()
  y = []
  yy = pd.DataFrame( df.isnull().sum()
                     , columns = ["missing"]
                   ).transpose()
  return yy.append( x )

def dwmParamByGroup (describeParam, groupParam, df):
  theGroups = df.groupby(groupParam)
  dfs = [ theGroups . get_group(x) [describeParam]
          . rename( columns = {describeParam : str(x) } )
          for x in theGroups.groups]
  return describeWithMissing( pd.concat( dfs,axis=1 ) )

def compareDescriptives(dfDict):
  for dfName in dfDict.keys():
    df = dfDict[ dfName ]
    print(dfName)
    print( describeWithMissing( df ).round(2) )

def compareDescriptivesByFourColumns(dfDict):
  colnames = dfDict[ list( dfDict.keys()
                         ) [0]
                   ].columns.values
  for i in range( math.ceil( len(colnames)/4 ) ):
    dfDict2 = {k: v[ colnames[4*i:4*i+4] ]
               for k, v in dfDict.items()
              }
    compareDescriptives( dfDict2 )
