# PITFALL: This validates the (user-provided) VAT rates,
# but not the (user-provided) marginal tax rates,
# as the latter are validated in Haskell, by
# haskell/MarginalTaxRatesToPython.hs

if True:
  import pandas as pd
  #
  import python.build.classes    as cla
  import python.build.output_io  as oio
  import python.common.common    as common
  import python.common.misc      as misc


def test_coicop_data( df : pd.DataFrame ):
  for t in [ cla . InRange ( 1e6, 2e7 ),
             cla . CoversRange ( 2e6, 1e7 ) ]:
    assert t.test ( df [ "coicop" ] )
  for col in ["vat","vat, min", "vat, max"]:
    assert ( cla . InRange ( 0, 1 ) .
             test ( df [ col ] ) )

def test_capitulo_c_data( df : pd.DataFrame ):
  for t in [ cla . InRange ( 1, 25 ),
             cla . CoversRange ( 1, 25 ) ]:
    assert t.test ( df [ "CODE" ] )
  for col in ["vat","vat, min", "vat, max"]:
    assert ( cla . InRange ( 0, 1 ) .
             test ( df [ col ] ) )

if True:
  test_coicop_data (
      misc . read_csv_or_xlsx (
          common . vat_by_coicop ) )
  test_capitulo_c_data (
      misc . read_csv_or_xlsx (
          common . vat_by_capitulo_c ) )
  oio.test_write(
      1, # PTIFALL: Uses no sample-size-dependent data,
         # so always writes to recip-1/
      "rate_input", "" )
