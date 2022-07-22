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

      # The special motorcycle tax, abusivelyed lump into the VAT table,
      # means the max "vat" is 0.27 rather than 0.19.
      "vat"              : cl.InRange( 0, 0.3 ),
      "vat frac"         : cl.InRange( 0, 0.3 / 1.3 ),
    }

  for k,v in inRange_spec.items():
    assert v.test( df[k] )

  coversRange_spec = {
    "household"        : cl.CoversRange( 2e5,6e5 ),
    "per month"        : cl.CoversRange( 0.05,30 ),
    "quantity"         : cl.CoversRange( 1,100 ),
    "value"            : cl.CoversRange( 3,1e6 ),
    "weight"           : cl.CoversRange( 10, 1000 ),
    "where-got"        : cl.CoversRange( 1,25 ),

    # The special motorcycle tax, abusively lump into the VAT table,
    # means the max "vat" is 0.27 rather than 0.19.
    # *However*, in the smaller samples,
    # we can't be sure that whole range is covered:
    # there  might be no motorcycle purchases.
    # That at least some purchase incurs a VAT of 0.19, though, is a safe bet.
    "vat frac"         : cl.CoversRange( 0, 0.19 / 1.19 ),
    "vat paid"         : cl.CoversRange( 0, 1e5 ),
    "vat"              : cl.CoversRange( 0, 0.19 ),
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
             , "vat paid"
             , "vat" ]
  very = [ "where-got" ]
  def all_columns ():
    # PITFALL: mypy doesn't seem to recognize that Python lets you define
    # functions in a class that are properties of the class
    # rather than some object belonging to it.
    # It wants this function to have an argument, presumably `self` --
    # but change it to that and this library break,
    # at the assertion
    #   assert ( set( df.columns ) ==
    #            set( Purchase_2_Columns_missing.all_columns() ) )
    # below.
    return ( Purchase_2_Columns_missing.very +
             Purchase_2_Columns_missing.slightly +
             Purchase_2_Columns_missing.never +
             Purchase_2_Columns_missing.purchase_codes )

def test_output( df ):
  log = "test_output()\n"

  assert unique ( df . columns )

  assert near (
    len ( df ),
    num_purchases_surviving / com . subsample,
    tol_frac = ( 1 / 10 if not com.subsample == 10
                 else 0.6 ) )
# TODO | BUG? Why is the previous conditional necessary? That is, why,
# in the special case of subsample = 1/10, is the size of the
# purchase data so different from what you'd expect.
# This isn't necessarily wrong, since the data is subsampled by households,
# and households can make different numbers of purchases.
# That's why `tol_frac` needs to be substantial in both cases.
# But it's surprising, because for subsample = 10,
# the reality is much less than the expectation.

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
             < 0.25 )

  return log


if True: # IO
  log = "starting\n"
  ps = oio.readUserData( com.subsample
                    , "purchases_2_vat." + com.strategy_suffix )
  log += test_ranges( ps )
  log += test_output( ps )
  oio.test_write( com.subsample
                , "build_purchases_2_vat"
                , log )
