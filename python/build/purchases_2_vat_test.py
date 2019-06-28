import pandas as pd
import numpy as np

import python.common.cl_args as cl
import python.build.output_io as oio


if True: # initialize log
  test_output_filename = "build_purchases_2_vat"
  oio.test_clear( cl.subsample
                , test_output_filename )
  def echo( content ):
    oio.test_write( cl.subsample
                  , test_output_filename
                  , content )
  echo( ["starting"] )


def test_ranges( df ):
  spec = {
      "25-broad-categs" : { cla.IsNull(), cla.InRange( 1, 25 ) }
    , "coicop"          : { cla.IsNull(), cla.InRange( 1e6, 2e7 ) }
    , "freq"            : { cla.IsNull(), cla.InRange( 1/36 - 0.001, 31 ) }
    , "household"       : { cla.IsNull(), cla.InRange( 0, 1e6 ) }
    ## >>> RESUME here
  }
  for k in spec:
    echo( [k] )
    assert cla.properties_cover_num_column( spec[k], df[k] )


class Purchase_2_Columns_missing:
  purchase_codes = [ "25-broad-categs"
                   , "coicop"]

  never = [ "big-hog"
          , "freq"
          , "freq-code"
          , "household"
          , "household-member"
          , "quantity"
          , "value"
          , "weight" ]

  slightly = [ "is-purchase"
             , "vat frac"
             , "vat frac, max"
             , "vat frac, min"
             , "vat paid, max"
             , "vat paid, min"
             , "vat"
             , "vat, max"
             , "vat, min" ]

  very = [ "where-got" ]

  def all_columns():
    return ( Purchase_2_Columns_missing.very +
             Purchase_2_Columns_missing.slightly +
             Purchase_2_Columns_missing.never +
             Purchase_2_Columns_missing.purchase_codes )

def test_output( df ):
  assert ( set( df.columns ) ==
           set( Purchase_2_Columns_missing.all_columns() ) )

  # coicop and 25-broad-categs are each individually missing substantially,
  # but exactly one of them is always present
  assert len( df[ ( ~ pd.isnull( df["coicop"]          ) ) &
                  ( ~ pd.isnull( df["25-broad-categs"] ) )
            ] ) == 0
  assert len( df[ (   pd.isnull( df["coicop"]          ) ) |
                  (   pd.isnull( df["25-broad-categs"] ) )
            ] ) == len(df)

  for c in Purchase_2_Columns_missing.never:
    assert ( len( df[ pd.isnull( df[c] ) ] )
             == 0 )

  for c in Purchase_2_Columns_missing.slightly:
    assert ( ( len( df[ pd.isnull( df[c] ) ] ) /
               len( df ) )
             < 0.02 )

  for c in Purchase_2_Columns_missing.very:
    assert ( ( len( df[ pd.isnull( df[c] ) ] ) /
               len( df ) )
             < 0.2 )


if True: # run tests
  ps = oio.readStage( cl.subsample
                    , "purchases_2_vat." + cl.strategy_suffix )
  test_output( ps )
