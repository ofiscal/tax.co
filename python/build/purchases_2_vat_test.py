if True:
  import pandas as pd
  import numpy as np
  #
  import python.build.classes as cl
  import python.common.common as cm
  import python.build.output_io as oio


def test_ranges( df ):
  log = "test_ranges()\n"
  per_cell_spec = {
      "25-broad-categs"  : { cl.IsNull(), cl.InRange( 1, 25 ) }
    , "big-hog"          : {              cl.InRange( 0, 1 ) }
    , "coicop"           : { cl.IsNull(), cl.InRange( 1e6, 2e7 ) }
    , "freq-code"        : {              cl.InRange( 0, 10 ) }
    , "household"        : { cl.IsNull(), cl.InRange( 0, 1e6 ) }
    , "household-member" : {              cl.InRange( 1, 230 ) }
    , "is-purchase"      : { cl.IsNull(), cl.InRange( 0, 1 ) }
    , "per month"        : {              cl.InRange( 1/36 - 0.001, 31 ) }
    , "quantity"         : {              cl.InRange( 0, 3e5 ) }
    , "value"            : {              cl.InRange( 0, 2e9 ) }
    , "vat"              : { cl.IsNull(), cl.InRange( 0, 0.271 ) }
    , "vat frac"         : { cl.IsNull(), cl.InRange( 0, 0.271 / 1.271 + 0.01 ) }
    , "vat frac, max"    : { cl.IsNull(), cl.InRange( 0, 0.271 / 1.271 + 0.01 ) }
  }

  ## >>> RESUME here. Remaining columns:
  # per_column_spec = {
    # "household" :
    # "household-member"
    #"per month"
    # "quantity"
    # "value"
    # "vat"
    # "vat frac"
    # "vat frac, max"
    # vat frac, min
    # vat paid, max
    # vat paid, min
    # vat, max
    # vat, min
    # weight
    # where-got }

  for k in per_cell_spec:
    assert cl.properties_cover_num_column( per_cell_spec[k], df[k] )

  return log


class Purchase_2_Columns_missing:
  purchase_codes = [ "25-broad-categs"
                   , "coicop"]

  never = [ "big-hog"
          , "per month"
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
  log = "test_output()\n"
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
             < 0.03 )

  for c in Purchase_2_Columns_missing.very:
    assert ( ( len( df[ pd.isnull( df[c] ) ] ) /
               len( df ) )
             < 0.2 )

  return log


if True: # IO
  log = "starting\n"
  ps = oio.readStage( cm.subsample
                    , "purchases_2_vat." + cm.strategy_suffix )
  log += test_ranges( ps )
  log += test_output( ps )
  oio.test_write( cm.subsample
                , "build_purchases_2_vat"
                , log )
