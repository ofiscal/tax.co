import numpy as np
import pandas as pd

import python.build.classes as cla


def test_Property_subclasses():
  assert True == cla.properties_cover_num_column(
    [ cla.InRange(0,1) ]
    , pd.Series( [0,0.5,1] ) )

  assert False == cla.properties_cover_num_column(
    [ cla.InRange(0,1) ]
    , pd.Series( [np.nan, 0,0.5,1] ) )

  assert True == cla.properties_cover_num_column(
    [ cla.InRange(0,1)
      , cla.IsNull() ]
    , pd.Series( [np.nan, 0,0.5,1] ) )

  assert ( pd.Series(               [True, True, False, False] )
         . equals( cla.InSet( {1,2} )
                 . test( pd.Series( [   1,    2,     3,np.nan] ) ) ) )

def test_re_nonNumeric():
  assert(      cla.re_nonNumeric.match( "1-" ) )
  assert( not( cla.re_nonNumeric.match( "-1" ) ) )
  assert(      cla.re_nonNumeric.match( " 1.#!,0 " ) )
  assert( not( cla.re_nonNumeric.match( " 1.34 0 " ) ) )

def test_re_white():
  assert(      cla.re_white.match( " db db " ) )
  assert( not( cla.re_white.match( " dbdb "  ) ) )

def test_re_digits():
  assert( cla.re_digits.match( ".21" ) )

def test_re_p():
  assert not( cla.re_p.match( "11213421,5" ) )
  assert      cla.re_p.match( "1.213421,5" )

def test_re_c():
  assert not( cla.re_c.match( "11213421.5" ) )
  assert      cla.re_c.match( "1.213421,5" )

def test_re_gt1p():
  assert( cla.re_gt1p.match( "1.213.421,5" ) )

def test_re_gt1c():
  assert( cla.re_gt1c.match( "1,213,421.5" ) )

def test_stringProperties():
  assert( cla.stringProperties( pd.Series( [0,1] ) ) ==
          { cla.StringProperty.NotAString } )
  assert( cla.stringProperties( pd.Series( ["a a", " b "] ) ) ==
          { cla.StringProperty.NonNumeric
          , cla.StringProperty.InteriorSpace} )
  assert( cla.stringProperties( pd.Series( ["0.1.2", "0.1"] ) ) ==
          { cla.StringProperty.Digits
          , cla.StringProperty.ManyPeriods} )
  assert( cla.stringProperties( pd.Series( ["0,2", "0.1"] ) ) ==
          { cla.StringProperty.Digits
          , cla.StringProperty.Period
          , cla.StringProperty.Comma } )
  assert( cla.stringProperties( pd.Series( ["12709901", "inv02"] ) ) ==
          { cla.StringProperty.Digits
          , cla.StringProperty.NonNumeric } )

def test_Correction():
  assert ( cla.Correction.Create_Constant_Column("b",1)
         . correct( pd.DataFrame( { "a" : [1,2,np.nan] } ) )
         . equals(  pd.DataFrame( { "a" : [1,2,np.nan]
                                  , "b" : [1,1,1] } ) ) )

  assert ( cla.Correction.Rename_Column("a","b")
         . correct( pd.DataFrame( { "a" : [1,2,np.nan] } ) )
         . equals(  pd.DataFrame( { "b" : [1,2,np.nan] } ) ) )

  assert ( cla.Correction.Replace_In_Column("a", {1:2})
         . correct( pd.DataFrame( { "a" : [1,2,np.nan] } ) )
         . equals(  pd.DataFrame( { "a" : [2,2,np.nan] } ) ) )

  assert ( cla.Correction.Replace_Missing_Values("a",3)
         . correct( pd.DataFrame( { "a" : [1,2,np.nan] } ) )
         . equals(  pd.DataFrame( { "a" : [1.,2.,3.] } ) ) )

  assert ( cla.Correction.Replace_Substring_In_Column("a","b","xx")
         . correct( pd.DataFrame( { "a" : ["1","ab" ,np.nan] } ) )
         . equals( pd.DataFrame( {  "a" : ["1","axx",np.nan] } ) ) )

  assert ( cla.Correction.Apply_Function_To_Column("a", lambda x: x+1)
         . correct( pd.DataFrame( { "a" : [1,2,np.nan]
                                  , "b" : [5,5,5] } ) )
         . equals( pd.DataFrame(  { "a" : [2,3,np.nan]
                                  , "b" : [5,5,5] } ) ) )

  assert ( cla.Correction.Drop_Row_If_Column_Satisfies_Predicate("a", lambda x: x>1)
         . correct( pd.DataFrame( { "a" : [0,1,2,np.nan]
                                  , "b" : [5,5,5,5] } ) )
         . equals( pd.DataFrame(  { "a" : [0,1,np.nan]
                                  , "b" : [5,5,5] }
                               , index = [0,1,3] ) ) )

  assert ( cla.Correction.Drop_Row_If_Column_Equals( "a", 1 )
         . correct( pd.DataFrame( { "a" : [0,1,2], "b" : [10,11,12] } ) )
         . equals(  pd.DataFrame( { "a" : [0,2], "b" : [10,12] }
                                , index = [0,2] ) ) )

  assert ( cla.Correction.Replace_Entirely_If_Substring_Is_In_Column(
             "a", "xx", "yy" )
         . correct( pd.DataFrame( { "a" : ["a","kxxk","xax"], "b" : [0,1,2] } ) )
         . equals(  pd.DataFrame( { "a" : ["a","yy","xax"],   "b" : [0,1,2] } ) ) )

  assert( cla.Correction.Drop_Column( "a" )
        . correct( pd.DataFrame( { "a" : ["a","kxxk","xax"], "b" : [0,1,2] } ) )
        . equals(  pd.DataFrame( {                           "b" : [0,1,2] } ) ) )

  assert( cla.Correction.Change_Column_Type( "a", str )
        . correct( pd.DataFrame( { "a" : [1,2,3], "b" : [0,1,2] } ) )
        . equals(  pd.DataFrame( { "a" : ["1","2","3"], "b" : [0,1,2] } ) ) )

def test_File():
  f = cla.File( "sassafrass"
              , "sassafrass.csv"
              , [("ugly input.csv","dirt","beautiful output.csv","gold")] )
  assert ( cla.name_map( f.col_specs )
           == { "ugly input.csv" : "beautiful output.csv" } )
  assert ( cla.input_map( f.col_specs )
           == { "ugly input.csv" : "dirt" } )
  assert ( cla.output_map( f.col_specs )
           == { "beautiful output.csv" : "gold" } )

if True: # run the tests
  test_Property_subclasses()
  test_re_nonNumeric()
  test_re_white()
  test_re_digits()
  test_re_p()
  test_re_c()
  test_re_gt1p()
  test_re_gt1c()
  test_stringProperties()
  test_File()
