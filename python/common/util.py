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

def myQuantile (
    n_quantiles : int, # Number of quantiles.
    in_col : pd.Series # The underlying variable to define quantiles from.
) -> pd.Series: # Series with index `in_col`, values quantiles 0 to n-1.
  quantile_length = len( str( n_quantiles - 1 ) )
    # quantile_length 1 <=> deciles, 2 <=> percentiles, 3 <=> miltiles, etc.
  return pd.qcut ( in_col,
                   n_quantiles,
                   labels = list( map(
                     lambda x: str(x) . zfill ( quantile_length ),
                     range ( 0, n_quantiles ) ) ),
                   duplicates = 'drop' )

def noisyQuantile(
    n_quantiles : int, # should be a power of 10
    noise_min : int,
    noise_max : int,
    in_col : pd.Series ):
  """
  UPDATE: This might be deprecated.
  It might cause undesirable reordering of households across quantiles
  in different runs of the sim.

  Noise guarantees the desired number of quantiles,
  of sizes as equal as possible.
  The nois is added to the underlying series,
  and should be very small relative to it.
  For instance, I use min=0 pesos, max=1 peso,
  and add that to peoples' income before generating income quantiles."""
  noise = pd.Series( np.random.uniform( noise_min, noise_max, len(in_col) ) )
  noise.index = in_col.index
  return myQuantile ( n_quantiles = n_quantiles,
                      in_col      = in_col + noise )

def printInRed(message):
    "from https://stackoverflow.com/a/287934/916142"
    CSI="\x1B["
    print( CSI+"31;40m" + message + CSI + "0m")

def print_trueBlack_falseRed( aBool, ifTrue, ifFalse ):
  if aBool: print( ifTrue )
  else: printInRed( ifFalse )
