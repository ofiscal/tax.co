import pandas as pd

import python.common.cl_args as cl
import python.build.output_io as oio


tolerance = 0.01

def test_vat_file( filename
                 , code_column_name
                 , fraction_that_should_be_non_null ):

  def non_null_part( column ):
    return column[ ~ pd.isnull( column ) ]

  df = oio.readStage( cl.subsample
                    , filename + "." + cl.strategy_suffix )

  assert set( df.columns ) == set(
    [code_column_name, 'vat'     , 'vat, min'     , 'vat, max'
                     , 'vat frac', 'vat frac, min', 'vat frac, max'] )

  for c in df.columns:
    if c == code_column_name:
          assert df[c].dtype == "int64"
    else: assert df[c].dtype == "float64"

  # The "vat" and "vat frac" columns might have a few missing values.
  # The others should have none.
  assert ( ( len( non_null_part( df["vat"] ) )
           / len( df ) )
         > ( fraction_that_should_be_non_null - tolerance ) )
  assert (  len( non_null_part( df["vat"] ) )
         == len( non_null_part( df["vat frac"] ) ) )
  df = df.drop( columns = ["vat", "vat frac"] )
  for c in df.columns:
    assert len( df[ ~ pd.isnull( df[c] ) ] ) == len( df )


if True: # run tests
  log = "starting\n"

  test_vat_file( "vat_coicop_brief", "coicop", 1031 / 1051 )
  test_vat_file( "vat_cap_c_brief", "25-broad-categs", 20 / 25 )

  oio.test_write( cl.subsample
                , "vat_rates"
                , log )
