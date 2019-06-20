import pandas as pd
import numpy as np

import python.common.cl_args as cl
import python.build.output_io as oio


if True: # initialize log
  test_output_filename = "build_purchases_2_vat"
  oio.test_clear( test_output_filename )
  def echo( content ):
    oio.test_write( test_output_filename
                  , content )
  echo( ["starting"] )


class Purchase_2_Columns:
  purchase_codes = [ "25-broad-categs"
                   , "coicop"]

  never_missing = [ "big-hog"
                  , "freq"
                  , "freq-code"
                  , "household"
                  , "household-member"
                  , "quantity"
                  , "value"
                  , "weight" ]

  slightly_missing =   [ "is-purchase"
                       , "vat frac"
                       , "vat frac, max"
                       , "vat frac, min"
                       , "vat paid, max"
                       , "vat paid, min"
                       , "vat"
                       , "vat, max"
                       , "vat, min" ]

  very_missing = [ "where-got" ]

def all_columns():
  return ( Purchase_2_Columns.very_missing +
           Purchase_2_Columns.slightly_missing +
           Purchase_2_Columns.never_missing +
           Purchase_2_Columns.purchase_codes )

def test_output( df ):
  assert ( set( df.columns ) ==
           set( all_columns() ) )

  # coicop and 25-broad-categs are each individually missing substantially,
  # but exactly one of them is always present
  assert len( df[ ( ~ pd.isnull( df["coicop"]          ) ) &
                  ( ~ pd.isnull( df["25-broad-categs"] ) )
            ] ) == 0
  assert len( df[ (   pd.isnull( df["coicop"]          ) ) |
                  (   pd.isnull( df["25-broad-categs"] ) )
            ] ) == len(df)

  for c in Purchase_2_Columns.never_missing:
    assert ( len( df[ pd.isnull( df[c] ) ] )
             == 0 )

  for c in Purchase_2_Columns.slightly_missing:
    assert ( ( len( df[ pd.isnull( df[c] ) ] ) /
               len( df ) )
             < 0.02 )

  for c in Purchase_2_Columns.very_missing:
    assert ( ( len( df[ pd.isnull( df[c] ) ] ) /
               len( df ) )
             < 0.2 )


if True: # run tests
  ps = oio.readStage( cl.subsample
                    , "purchases_2_vat." + cl.strategy_suffix )
  test_output( ps )
