# TODO ? Ideally, the column-specifying "quads" used below
# would be their own separate type,
# but that would mean rewriting all the code that appends them.

# TODO ? divide into submodules

import enum
from   functools import reduce
import math
import numpy as np
import pandas as pd
import pytest
import re
import sys


#############################
### properties of numbers ###
#############################

class SeriesProperty:
  """When test() is run on a series, it returns a single boolean."""
  def test( self, series : pd.Series ) -> bool:
    raise NotImplementedError("SeriesProperty is an abstract class.")

class CoversRange(SeriesProperty):
  """Similar to InRange. If c = CoversRange(x,y), and s is a series, then s passes c.test() if and only if c includes a value less than x and a value greater than y."""
  def __init__( self, floor, ceiling ):
    self.floor = floor
    self.ceiling = ceiling
  def test( self, series : pd.Series ) -> bool:
    return ( (series >= self.ceiling).any() &
             (series <= self.floor).any() )

class MeanBounds ( SeriesProperty ) :
  """MeanBounds(a,b) will test that the mean of a series is between a and b."""
  def __init__( self, floor, ceiling ):
    self.floor = floor
    self.ceiling = ceiling
  def test( self, series : pd.Series ) -> bool:
    """Bounds equal to infinity are a little annoying."""
    m = series.mean()
    if np.isnan(m): return False
    floorTest = ( True if self.floor == -np.inf else (
        m == np.inf if self.floor == np.inf else (
            m >= self.floor ) ) )
    ceilingTest = ( True if self.ceiling == np.inf else (
        m == -np.inf if self.ceiling == -np.inf else (
            m <= self.ceiling ) ) )
    return floorTest & ceilingTest

class MissingAtMost(SeriesProperty):
  """MissingAtMost(f) tests that a fraction at most f of the values in a series are missing. f should be in [0,1]."""
  def __init__( self, fracMissing ):
    self.fracMissing = fracMissing
  def test( self, series : pd.Series ) -> bool:
    return series . isnull () . mean () <= self . fracMissing

class InRange(SeriesProperty):
  """If c = InRange(x,y), and s is a series, then s passes c.test() if and only if c includes no value less than x and no value greater than y."""
  def __init__( self, floor, ceiling ):
    self.floor = floor
    self.ceiling = ceiling
  def test( self, series : pd.Series ) -> pd.Series:
    s = series.dropna()
    return ( (s <= self.ceiling)
           & (s >= self.floor) ) . all()

class InSet(SeriesProperty):
  def __init__( self, values : set ):
    self.values = values
  def test( self, series : pd.Series ) -> pd.Series:
    s = series.dropna()
    return s . isin( self.values ) . all()


#############################
### properties of strings ###
#############################

class StringCellProperty(enum.Flag):
  NotAString    = enum.auto()
  HasNull       = enum.auto() # PITFALL: A non-string column will generate
    # nothing but "NotAString", even if it does have null values.
  Digits        = enum.auto()
  InteriorSpace = enum.auto()
  NonNumeric    = enum.auto()
  Period        = enum.auto()
  Comma         = enum.auto()
  ManyPeriods   = enum.auto()
  ManyCommas    = enum.auto()

if True: # TODO ? WART: These should be defined within each enum type,
  # or if that's awkward,
  # group them into one function that takes an enum as an argument,
  # to simplify the namespace.
  re_nonNumeric = re.compile( "(.+\-|.*[^0-9\s\.,\-])" )
    # A (-) is nonnumeric if anything precedes it.
    # Any [^0-9\s\.,\-] is nonnumeric.
  re_white      = re.compile( ".*[^\s].*\s.*[^\s]" )
  re_digits     = re.compile( ".*[0-9]" )
  re_p          = re.compile( ".*\." )
  re_c          = re.compile( ".*," )
  re_gt1p       = re.compile( ".*\..*\." )
  re_gt1c       = re.compile( ".*,.*," )

def stringProperties( column ):
  """Seems to (?) determine all properties that apply to a string column. See classes_test.py."""
  # let c = column.apply( str.strip )
    # omitted because this is done to every column when subsampling
  if column.dtype not in [object]:
    return {StringCellProperty.NotAString}

  acc = set()
  for (_,val) in column.iteritems():
    if pd.isnull( val ):
      acc.add( StringCellProperty.HasNull )
    else:
      for ( regex, flag ) in [
          ( re_digits, StringCellProperty.Digits )
          , ( re_white, StringCellProperty.InteriorSpace )
          , ( re_nonNumeric, StringCellProperty.NonNumeric )
          , ( re_p, StringCellProperty.Period )
          , ( re_c, StringCellProperty.Comma )
          , ( re_gt1p, StringCellProperty.ManyPeriods )
          , ( re_gt1c, StringCellProperty.ManyCommas ) ]:
        if regex.match( val ):
          acc.add( flag )

  if StringCellProperty.ManyPeriods in acc:
    acc.discard( StringCellProperty.Period )
  if StringCellProperty.ManyCommas in acc:
    acc.discard( StringCellProperty.Comma )

  return acc


#############################################################
### Files, and the Correction class for manipulating them ###
#############################################################

# TODO : rename Correction -> ModifyDataset
class Correction:
  """Ways to modify a dataset. Convenience functions for pandas routines.
Mostly of these functions affect a single column, but there are exceptions."""
  # PITFALL: Most of the `correct` functions defeined below are destructive, nxon-functional. Each one that is is marked as such with a `PITFALL` comment.
  class Create_Constant_Column:
    def __init__( self, col_name, value ):
      self.col_name = col_name
      self.value = value
    def correct( self, df ):
      # PITFALL: Non-functional. `df` (the input) changes even if
      # `df` (the output) is not assigned to anything.
      df[self.col_name] = self.value
      return df

  class Rename_Column:
    def __init__( self, old, new ):
      self.old = old
      self.new = new
    def correct( self, df ):
      # PITFALL: Non-functional. `df` (the input) changes even if
      # `df` (the output) is not assigned to anything.
      return df.rename( columns = {self.old : self.new} )

  class Replace_In_Column:
    # Anything not mentioned in the dictionary is left unchanged.
    def __init__( self, col_name, dct ):
      self.col_name = col_name
      self.dct = dct
    def correct( self, df ):
      # PITFALL: Non-functional. `df` (the input) changes even if
      # `df` (the output) is not assigned to anything.
      df[self.col_name] = ( df[self.col_name]
                          . replace( self.dct ) )
      return df

  class Replace_Missing_Values:
    def __init__( self, col_name, value ):
      self.col_name = col_name
      self.value = value
    def correct( self, df ):
      # PITFALL: Non-functional. `df` (the input) changes even if
      # `df` (the output) is not assigned to anything.
      df[self.col_name] = ( df[self.col_name]
                          . fillna( self.value
                          # , inplace = True
                          ) )
      return df

  class Replace_Substring_In_Column:
    def __init__( self, col_name, before, after ):
      self.col_name = col_name
      self.before = before
      self.after = after
    def correct( self, df ):
      # PITFALL: Non-functional. `df` (the input) changes even if
      # `df` (the output) is not assigned to anything.
      c = self.col_name
      df[c] = ( df[c]
              . astype(str)
              . str.replace( self.before, self.after ) )
      # The previous line converts np.nan to "nan" (the string); the next fixes that.
      # PITFALL: If a cell actually should be the string "nan", this needs complication.
      df.loc[ df[c] == "nan", c] = np.nan
      return df

  class Apply_Function_To_Column:
    def __init__( self, col_name, func ):
      self.col_name = col_name
      self.func = func
    def correct( self, df ):
      # PITFALL: Non-functional. `df` (the input) changes even if
      # `df` (the output) is not assigned to anything.
      df[self.col_name] = ( df[self.col_name]
                            .apply(self.func) )
      return df

  class Drop_Row_If_Column_Satisfies_Predicate:
    def __init__( self, col_name, pred ):
      self.col_name = col_name
      self.pred = pred
    def correct( self, df ):
      return df.drop(
        df[ self.pred( df[self.col_name] )
        ].index
      )

  class Drop_Row_If_Column_Equals:
    def __init__( self, col_name, value ):
      self.col_name = col_name
      self.value = value
    def correct( self, df ):
      return df.drop(
        df[
          df[self.col_name] == self.value
        ] . index
      )

  class Replace_Entirely_If_Substring_Is_In_Column:
    def __init__( self, col_name, substring, replacement ):
      self.col_name = col_name
      self.substring = substring
      self.replacement = replacement
    def correct( self, df ):
      # PITFALL: Non-functional. `df` (the input) changes even if
      # `df` (the output) is not assigned to anything.
      df.loc[ (~ df[self.col_name].isna() )
              & df[self.col_name].str.contains( self.substring )
            , self.col_name
            ] = self.replacement
      return df

  class Drop_Column:
    def __init__( self, col_name ):
      self.col_name = col_name
    def correct( self, df ):
      return df.drop( self.col_name, axis = 'columns' )

  class Change_Column_Type:
    def __init__( self, col_name, new_type ):
        # PITFALL: new_type should be, e.g., str, not "str"
      self.col_name = col_name
      self.new_type = new_type
    def correct( self, df ):
      # PITFALL: Non-functional. `df` (the input) changes even if
      # `df` (the output) is not assigned to anything.
      df[self.col_name] = df[self.col_name] . astype(self.new_type)
      return df

class File:
  # TODO: Rename this EnphFile.
  """Describes a file from the ENPH. See, e.g., ./build/purchases/nice_purchases.py."""
  def __init__( self, name, filename, col_specs, corrections=[] ):
    self.name = name
    self.filename = filename
    self.col_specs = col_specs # a list (or set) of
      # (old name, input format, new name, output format) tuples,
      # where each format is a list (or set) of StringCellProperty enum values.
    self.corrections = corrections

def name_map(quads):
  """input: a collection of col_specs 4-tuples.
output: a map from old names to new names. """
  return { t[0]:t[2] for t in quads }
def input_map(quads):
  """input: a collection of col_specs 4-tuples.
output: a map from old names to the formats they are believed to be in. """
  return { t[0]:t[1] for t in quads }
def output_map(quads):
  """input: a collection of col_specs 4-tuples.
output: a map from new names to the format they should (eventually) be in. """
  return { t[2]:t[3] for t in quads }
