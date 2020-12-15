import pandas as pd
import python.common.common as common
import python.build.classes as cla


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
  test_coicop_data(
      pd.read_csv( common.vat_by_coicop, sep=";" ) )
  test_capitulo_c_data(
      pd.read_csv( common.vat_by_capitulo_c ) )

