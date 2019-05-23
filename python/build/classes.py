# TODO ? Ideally, the column-specifying "quads" used below
# would be their own separate type,
# but that would mean rewriting all the code that appends them.

import enum
from   functools import reduce
import math
import numpy as np
import pandas as pd
import pytest
import re
import sys


### properties of numbers ###

class NumProperty:
  pass

class IsNull(NumProperty):
  def test(self,cell):
    return pd.isnull( cell )

class InRange(NumProperty):
  def __init__(self,floor,ceiling):
    self.floor = floor
    self.ceiling = ceiling
  def test(self,cell):
    return ( (cell <= self.ceiling)
           & (cell >= self.floor) )

def properties_cover_num_column( properties, column ):
  def properties_cover_num_cell( cell ):
    for p in properties:
      if p.test( cell ): return True
    return False
  return ( column.apply( properties_cover_num_cell )
         . all() )


### properties of strings ###

class StringProperty(enum.Flag):
  NotAString    = enum.auto()
  HasNull       = enum.auto()
  Digits        = enum.auto()
  InteriorSpace = enum.auto()
  NonNumeric    = enum.auto()
  Period        = enum.auto()
  Comma         = enum.auto()
  ManyPeriods   = enum.auto()
  ManyCommas    = enum.auto()

if True:
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
  # let c = column.apply( str.strip )
    # omitted because this is done to every column when subsampling
  if column.dtype not in [object]:
    return {StringProperty.NotAString}

  acc = set()
  for (_,val) in column.iteritems():
    if pd.isnull( val ):
      acc.add( StringProperty.HasNull )
    else:
      for ( regex, flag ) in [
          ( re_digits, StringProperty.Digits )
          , ( re_white, StringProperty.InteriorSpace )
          , ( re_nonNumeric, StringProperty.NonNumeric )
          , ( re_p, StringProperty.Period )
          , ( re_c, StringProperty.Comma )
          , ( re_gt1p, StringProperty.ManyPeriods )
          , ( re_gt1c, StringProperty.ManyCommas ) ]:
        if regex.match( val ):
          acc.add( flag )

  if StringProperty.ManyPeriods in acc:
    acc.discard( StringProperty.Period )
  if StringProperty.ManyCommas in acc:
    acc.discard( StringProperty.Comma )

  return acc


### files ###

class Correction:
  # PITFALL: Some of the return statements in the implementations of "correct" below are unnecessary,
    # because the operations before them are destructive. However, "drop" is not destructive.
    # For compatibility with Drop_Row_If_Column_Satisfies_Predicate, therefore, every "correct" function
    # must return the data frame it operates on.

  class Create_Constant_Column:
    def __init__(self,col_name,value):
      self.col_name = col_name
      self.value = value
    def correct(self,df):
      df[self.col_name] = self.value
      return df

  class Rename_Column:
    def __init__(self,old,new):
      self.old = old
      self.new = new
    def correct(self,df):
      return df.rename( columns = {self.old : self.new} )

  class Replace_In_Column:
    # Anything not mentioned in the dictionary is left unchanged.
    def __init__(self,col_name,dct):
      self.col_name = col_name
      self.dct = dct
    def correct(self,df):
      df[self.col_name] = ( df[self.col_name]
                          . replace( self.dct ) )
      return df

  class Replace_Missing_Values:
    def __init__(self,col_name,value):
      self.col_name = col_name
      self.value = value
    def correct(self,df):
      df[self.col_name] = df[self.col_name].fillna( self.value )
      return df

  class Replace_Substring_In_Column:
    def __init__(self,col_name,before,after):
      self.col_name = col_name
      self.before = before
      self.after = after
    def correct(self,df):
      df[self.col_name] = ( df[self.col_name]
                            .astype(str)
                            .str.replace( self.before, self.after ) )
      return df

  class Apply_Function_To_Column:
    def __init__(self,col_name,func):
      self.col_name = col_name
      self.func = func
    def correct(self,df):
      df[self.col_name] = ( df[self.col_name]
                            .apply(self.func) )
      return df

  class Drop_Row_If_Column_Satisfies_Predicate:
    def __init__(self,col_name,pred):
      self.col_name = col_name
      self.pred = pred
    def correct(self,df):
      return df.drop(
        df[ self.pred( df[self.col_name] )
        ].index
      )

  class Drop_Row_If_Column_Equals:
    def __init__(self,col_name,value):
      self.col_name = col_name
      self.value = value
    def correct(self,df):
      return df.drop(
        df[
          df[self.col_name] == self.value
        ] . index
      )

  class Replace_Entirely_If_Substring_Is_In_Column:
    def __init__(self,col_name,substring,replacement):
      self.col_name = col_name
      self.substring = substring
      self.replacement = replacement
    def correct(self,df):
      df.loc[ (~ df[self.col_name].isna() )
              & df[self.col_name].str.contains( self.substring )
            , self.col_name
      ] = self.replacement
      return df

  class Drop_Column:
    def __init__(self,col_name):
      self.col_name = col_name
    def correct(self,df):
      return df.drop( self.col_name, axis = 'columns' )

  class Change_Column_Type:
    def __init__(self,col_name,new_type):
        # PITFALL: new_type should be, e.g., str, not "str"
      self.col_name = col_name
      self.new_type = new_type
    def correct(self,df):
      df[self.col_name] = df[self.col_name] . astype(self.new_type)
      return df

class File:
  def __init__(self,name,filename,col_specs,corrections=[]):
    self.name = name
    self.filename = filename
    self.col_specs = col_specs # a list (or set) of
      # (old name, input format, new name, output format) tuples,
      # where each format is a list (or set) of StringProperty enum values.
    self.corrections = corrections

def name_map(quads):
  """ input: a collection of col_specs 4-tuples
      output: a map from old names to new names """
  return { t[0]:t[2] for t in quads }
def input_map(quads):
  """ input: a collection of col_specs 4-tuples
      output: a map from old names to the formats they are believed to be in """
  return { t[0]:t[1] for t in quads }
def output_map(quads):
  """ input: a collection of col_specs 4-tuples
      output: a map from new names to the format they should (eventually) be in """
  return { t[2]:t[3] for t in quads }
