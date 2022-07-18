if True:
  from typing import List, Dict
  import pandas as pd
  import numpy as np
  import math as math


def near( a : float,
          b : float,
          tol_abs  : float = 0.001,
          tol_frac : float = 0.001 ):
    if ( ( abs( a - b )
           < tol_abs ) |
         ( abs( a - b )
           <= (tol_frac * max( abs(a), abs(b) ) ) ) ):
        return True
    else: return False

def unique( coll : List ) -> bool:
  return len( coll ) == len( set( coll ) )

def tuple_by_threshold( income, schedule ):
  """If a "schedule" is a list of tuples, where the first element of each tuple gives \
  the threshold (least income) at which the regime described by the tuple applies, \
  this returns that triple. If the income is less than the first threshold, \
  the first threshold is returned. """
  if (   ( not( schedule[1:] ) ) # [] = False, nonempty list = True
       | (income < schedule[0][0] ) ):
      return schedule[0]
  highEnoughToBeHere = (income >= schedule[0][0])
  lowEnoughToBeHere = (income < schedule[1][0])
  if highEnoughToBeHere & lowEnoughToBeHere:
      return schedule[0]
  if True:
      return tuple_by_threshold( income, schedule[1:] )

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
