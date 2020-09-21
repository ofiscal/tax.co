if True:
  import pandas as pd
  import numpy  as np
  #
  import python.build.classes   as cl
  import python.build.output_io as oio
  import python.common.common   as com
  from   python.common.misc import num_purchases_surviving
  from   python.common.util import unique, near


def test_ranges( df ):
  log = "test_ranges()\n"

  inRange_spec = {
      "25-broad-categs"  : cl.InRange( 1, 25 ),
      "big-hog"          : cl.InRange( 0, 1 ),
      "coicop"           : cl.InRange( 1e6, 2e7 ),

      # PITFALL: "freq-code"=11 <=> the purchase is never made.
      # This corresponds to a "per month" value of np.nan.
      "freq-code"        : cl.InRange( 0, 10 ),
      "household"        : cl.InRange( 0, 1e6 ),
      "is-purchase"      : cl.InRange( 0, 1 ),
      "per month"        : cl.InRange( 1/36 - 0.001, 31 ),
      "quantity"         : cl.InRange( 0, 1e8 ),
      "value"            : cl.InRange( 0, 3e9 ),
      "vat frac"         : cl.InRange( 0, 0.271 / 1.271 + 0.01 ),
      "vat frac, max"    : cl.InRange( 0, 0.271 / 1.271 + 0.01 ),
      "vat"              : cl.InRange( 0, 0.271 )
    }

  for k,v in inRange_spec.items():
    assert v.test( df[k] )

  coversRange_spec = {
    "household"        : cl.CoversRange( 2e5,6e5 ),
    "per month"        : cl.CoversRange( 0.05,30 ),
    "quantity"         : cl.CoversRange( 1,100 ),
    "value"            : cl.CoversRange( 3,1e6 ),
    "vat frac"         : cl.CoversRange( 0, 0.159 ),
    "vat frac, max"    : cl.CoversRange( 0, 0.159 ),
    "vat frac, min"    : cl.CoversRange( 0, 0.159 ),
    "vat paid, max"    : cl.CoversRange( 0, 1e5 ),
    "vat paid, min"    : cl.CoversRange( 0, 1e5 ),
    "vat"              : cl.CoversRange( 0,0.19 ),
    "vat, max"         : cl.CoversRange( 0, 0.19 ),
    "vat, min"         : cl.CoversRange( 0, 0.19 ),
    "weight"           : cl.CoversRange( 10, 1000 ),
    "where-got"        : cl.CoversRange( 1,25 )
    }

  for k,v in coversRange_spec.items():
    assert v.test( df[k] )

  return log


class Purchase_2_Columns_missing:
  purchase_codes = [ "25-broad-categs"
                   , "coicop"]

  never = [ "big-hog"
          , "per month"
          , "freq-code"
          , "household"
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

  assert unique( df.columns )

  assert near(
    len(df),
    num_purchases_surviving / com.subsample,
    tol_frac = 1/10 )

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
  ps = oio.readStage( com.subsample
                    , "purchases_2_vat." + com.strategy_suffix )
  log += test_ranges( ps )
  log += test_output( ps )
  oio.test_write( com.subsample
                , "build_purchases_2_vat"
                , log )
