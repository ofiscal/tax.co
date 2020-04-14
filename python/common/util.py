if True:
  from typing import List, Dict
  import pandas as pd
  import numpy as np
  import math as math

def near( a : float,
          b : float,
          tol_abs  : float = 1,
          tol_frac : float = 0.001 ):
    if ( ( abs( a - b )
           < tol_abs ) |
         ( abs( a - b )
           <= (tol_frac * max( abs(a), abs(b) ) ) ) ):
        return True
    else: return False

def unique( coll: List ) -> bool:
  return len( coll ) == len( set( coll ) )

def tuple_by_threshold( income, schedule ):
  """If a "schedule" is a list of tuples, where the first element of each tuple gives \
  the threshold (least income) at which the regime described by the tuple applies, \
  this returns that triple."""
  if not( schedule[1:] ):     # [] = False, nonempty list = True
    return schedule[0]
  elif (income >= schedule[0][0]) & (income < schedule[1][0]):
    return schedule[0]
  else: return tuple_by_threshold( income, schedule[1:] )

def pad_column_as_int( length, column ):
  """ Left-pads a column's numbers with zeroes, to have the desired length.
  Delete any trailing ".0". Leave NaN unchanged."""
  format_str = '{0:0>' + str(length) + '}'
  c = column.copy()
  c[ ~ pd.isnull( c ) ] = (
    c[ ~ pd.isnull( c ) ]
    . apply( lambda s:
             format_str.format(
               str(s)
               . replace( ".0", "" ) )
    ) )
  return c

def interpretCategorical( column, categories ):
  return pd.Categorical( column
                       , categories = categories
                       , ordered = True)

def noisyQuantile( n_quantiles, noise_min, noise_max, in_col ):
  "Noise guarantees the desired number of quantiles, of sizes as equal as possible."
  noise = pd.Series( np.random.uniform( noise_min, noise_max, len(in_col) ) )
  noise.index = in_col.index
  quantile_length = len( str( n_quantiles - 1 ) )
  return pd.qcut( in_col + noise
                , n_quantiles
                , labels = list( map(
                    lambda x: str(x).zfill(quantile_length)
                  , range(0,n_quantiles) ) )
                , duplicates = 'drop' )

def printInRed(message):
    "from https://stackoverflow.com/a/287934/916142"
    CSI="\x1B["
    print( CSI+"31;40m" + message + CSI + "0m")

def print_trueBlack_falseRed( aBool, ifTrue, ifFalse ):
  if aBool: print( ifTrue )
  else: printInRed( ifFalse )


# Keeping this only to avoid breaking vat/report/*.py
# tabulate_stats_by_group is better, because it:
#   takes missing values into account
#   includes means
#   includes statistics on nonzero values
#   does not modify its arguments
def tabulate_min_median_max_by_group(df, group_name, param_name):
    dff = df.copy()
    dff["one"] = 1
    counts = dff.groupby( group_name )[["one"]]               \
           .agg('sum').rename(columns = {"one":"count"})
    mins = dff.groupby( group_name )[[param_name]]            \
           .agg('min').rename(columns = {param_name:"min"})
    medians = dff.groupby( group_name )[[param_name]]         \
           .agg('median').rename(columns = {param_name:"median"})
    maxs = dff.groupby( group_name )[[param_name]]     \
           .agg('max').rename(columns = {param_name:"max"})
    return pd.concat([counts,mins,maxs,medians],axis=1)

def tabulate_stats_by_group(df0, group_name, param_name, weight_name=None):
  """ Alas, Pandas offers no easy way to compute weighted medians. """
  if weight_name != None:
    df = df0[ ~ df0[param_name].isnull() ].copy()
    total_weight = df[weight_name].sum()
    df["val*weight"] = df[param_name] * df[weight_name]
    total_weighted_value = df["val*weight"].sum()
    num_obs = len( df )
    df_no_0 = df[ df[param_name] != 0 ]

    # This is a weighted count. See the comment in the test code
    # for an example of what that means.
    counts = df         . groupby( group_name ) [[weight_name
             ]]         . agg( 'sum'
             )          . rename( columns = {"weight":"count"}
             )          * (num_obs / total_weight)
    nonzeros = df_no_0  . groupby( group_name ) [[weight_name
             ]]         . agg('sum'
             )          . rename(columns = {"weight":"nonzero"}
             )          * (num_obs / total_weight)
    mins =     df       . groupby( group_name ) [[ param_name
             ]]         . agg('min'
             )          . rename(columns = {param_name:"min"})
    maxs =     df       . groupby( group_name ) [[ param_name
             ]]         . agg('max'
             )          . rename(columns = {param_name:"max"})

    shares =   df       . groupby( group_name ) [[ "val*weight"
             ]]         . agg('sum'
             )          . rename(columns = {"val*weight":"share"})
    shares["share"] = shares [ "share" ] / total_weighted_value

    means = df          . groupby( group_name ) [[ "val*weight", weight_name
             ]]         . agg('mean')
    means["mean"] = means [ "val*weight" ] / means[weight_name]
    means         = means . drop( columns = ["val*weight",weight_name] )

    means_nonzero = df_no_0 . groupby( group_name ) [[ "val*weight", weight_name
             ]]             . agg('mean')
    means_nonzero["mean_nonzero"] = means_nonzero[ "val*weight"
                                  ] / means_nonzero[weight_name]
    means_nonzero = means_nonzero.drop( columns = ["val*weight", weight_name] )
    medians = df.groupby( group_name ) [[param_name]]         \
           .agg('median').rename(columns = {param_name:"median_unweighted"})
    medians_nonzero = df[ df[param_name] != 0
                         ].groupby( group_name ) [[param_name
         ]].agg('median').rename(columns = {param_name:"median_nonzero_unweighted"})
    return pd.concat( [ counts, shares, mins, means, maxs, nonzeros, means_nonzero
                      , medians, medians_nonzero ]
                    , axis = 1 )

  else:
    df = df0[ ~ df0[param_name].isnull() ].copy()
    df["one"] = 1
    counts = df.groupby( group_name )[["one"]]               \
           .agg('sum').rename(columns = {"one":"count_unweighted"})
    nonzeros = df[ df[param_name] != 0
                 ].groupby( group_name )[["one"
         ]].agg('sum').rename(columns = {"one":"nonzero_unweighted"})
    mins = df.groupby( group_name )[[param_name]]            \
           .agg('min').rename(columns = {param_name:"min"})
    medians = df.groupby( group_name )[[param_name]]         \
           .agg('median').rename(columns = {param_name:"median_unweighted"})
    medians_nonzero = df[ df[param_name] != 0
                         ].groupby( group_name )[[param_name
         ]].agg('median').rename(columns = {param_name:"median_nonzero_unweighted"})
    maxs = df.groupby( group_name )[[param_name]]     \
           .agg('max').rename(columns = {param_name:"max"})

    shares = df. groupby( group_name ) [[ param_name
             ]] . agg('sum'
             )  . rename(columns = {param_name:"share"})
    shares["share"] = shares [ "share" ] / shares["share"].sum()

    means = df.groupby( group_name )[[param_name]]     \
           .agg('mean').rename(columns = {param_name:"mean_unweighted"})
    means_nonzero = df[ df[param_name] != 0
                         ].groupby( group_name )[[param_name
         ]].agg('mean').rename(columns = {param_name:"mean_nonzero_unweighted"})
    return pd.concat([counts, shares, nonzeros, mins, maxs
                      ,medians,medians_nonzero,means,means_nonzero],axis=1)

def histogram(series):
    dff = pd.DataFrame(series).copy()
    dff["one"] = 1
    counts = dff.groupby( series.name )[["one"]]               \
           .agg('sum').rename(columns = {"one":"count"})       \
        / series.count() # normalize
    return counts

def describeWithMissing(df):
  most_stats = df.describe()
  missing_stat = pd.DataFrame( df.isnull().sum()
                             , columns = ["missing"]
                             ).transpose()
  length_stat = pd.DataFrame( [[len(df) for _ in df.columns]]
                            , index = ["length"]
                            , columns = df.columns )
  nums = df.select_dtypes(include=[np.number]) # subset of the columns
  zeroes = pd.DataFrame( [nums.apply( lambda col: len( col[col==0] ) / len(nums) )] )
  return zeroes.append( length_stat.append( missing_stat.append( most_stats ) ) )

def compare_2_columns_from_different_tables (df1, colname1, df2, colname2):
  x = describeWithMissing( df1[[ colname1 ]] )
  y = describeWithMissing( df2[[ colname2 ]] )
  return pd.merge(x, y, left_index=True, right_index=True)

def dwmParamByGroup (describeParam, groupParam, df):
  "Like describeWithMissing, but by group, for a single parameter."
  theGroups = df.groupby( groupParam )
  dfs = [
      describeWithMissing (
        theGroups.get_group(x) [[describeParam]]
        . rename( columns = {describeParam : x } ) )
      for x in theGroups.groups.keys()]
  return pd.concat( dfs,axis=1 )

def dwmByGroup (groupParam, df):
  "Like describeWithMissing, but by group."
  for c in df.columns:
    print( "\n" + c )
    print( dwmParamByGroup( c, groupParam, df ) )

def compareDescriptives(dfDict):
  "builds a table of summary statistics for each data set in the input dictionary"
  for dfName in dfDict.keys():
    df = dfDict[ dfName ]
    print(); print()
    print( dfName )
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
  # TODO (#clean) summarizeQuantiles should not assume a column named "income".
  dff = df.copy()
  dff["one"] = 1
  dff = dff[ ~ dff["income"].isnull() ]
  counts = dff.groupby( quantileParam )[["one"]]     \
         .agg('sum').rename(columns = {"one":"count"})
  mins = dff.groupby( quantileParam )[["income"]]    \
         .agg('min').rename(columns = {"income":"min"})
  maxs = dff.groupby( quantileParam )[["income"]]    \
         .agg('max').rename(columns = {"income":"max"})
  return pd.concat([counts,mins,maxs],axis=1)
