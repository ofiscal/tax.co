import pandas as pd
import math as math

def printInRed(message):
    """from https://stackoverflow.com/a/287934/916142"""
    CSI="\x1B["
    print( CSI+"31;40m" + message + CSI + "0m")

def tabulate_min_median_max_by_group(df, group_name, param_name):
    dff = df
    dff["one"] = 1
    counts = df.groupby( group_name )[["one"]]               \
           .agg('sum').rename(columns = {"one":"count"})
    mins = df.groupby( group_name )[[param_name]]            \
           .agg('min').rename(columns = {param_name:"min"})
    medians = df.groupby( group_name )[[param_name]]         \
           .agg('median').rename(columns = {param_name:"median"})
    maxs = df.groupby( group_name )[[param_name]]     \
           .agg('max').rename(columns = {param_name:"max"})
    return pd.concat([counts,mins,maxs,medians],axis=1)

def tabulate_series(series):
    dff = pd.DataFrame(series)
    dff["one"] = 1
    counts = dff.groupby( series.name )[["one"]]               \
           .agg('sum').rename(columns = {"one":"count"})       \
        / series.count() # normalize
    return counts

def describeWithMissing(df):
  x = df.describe()
  y = []
  yy = pd.DataFrame( df.isnull().sum()
                     , columns = ["missing"]
                   ).transpose()
  return yy.append( x )

def compare_2_columns_from_different_tables (df1, colname1, df2, colname2):
  x = describeWithMissing( df1[[ colname1 ]] )
  y = describeWithMissing( df2[[ colname2 ]] )
  return pd.merge(x, y, left_index=True, right_index=True)

def dwmParamByGroup (describeParam, groupParam, df):
  theGroups = df.groupby(groupParam)
  dfs = [ theGroups . get_group(x) [describeParam]
          . rename( columns = {describeParam : str(x) } )
          for x in theGroups.groups]
  return describeWithMissing( pd.concat( dfs,axis=1 ) )

def compareDescriptives(dfDict):
  """ builds a table of summary statistics for each data set in the input dictionary """
  for dfName in dfDict.keys():
    df = dfDict[ dfName ]
    print(); print()
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

def summarizeQuantiles (quantileParam, df):
  # TODO : test: does this change df outside of the function?
  df["one"] = 1
  counts = df.groupby( quantileParam )[["one"]]     \
         .agg('sum').rename(columns = {"one":"count"})
  mins = df.groupby( quantileParam )[["income"]]    \
         .agg('min').rename(columns = {"income":"min"})
  maxs = df.groupby( quantileParam )[["income"]]    \
         .agg('max').rename(columns = {"income":"max"})
  return pd.concat([counts,mins,maxs],axis=1)
