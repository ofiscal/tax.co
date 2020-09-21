# PITFALL: buildings.py is only ever run on the full sample (see Makefile),
# so these tests can be more precise than ones covering multiple subsamples.

if True:
  import pandas as pd
  #
  import python.common.common as cl
  import python.common.util as util
  import python.build.output_io as oio
  from   python.common.util import unique
  import python.build.classes as cla


def test_types( df ):
  for (c,t) in [ ("household","int64")
               , ("region-1","O")
               , ("region-2","O")
               , ("estrato","float64")
               , ("recently bought this house", "bool")
               ]:
    assert df[c].dtype == t

def test_nullity( df ):
  for c in ["household",
            "region-1",
            "region-2",
            "recently bought this house"]:
    assert len( df[ pd.isnull( df[c] ) ] ) == 0

  for c in ["region-1","region-2"]:
    # none of these strings should be empty
    assert df[c].apply( lambda x: len(x) > 0
                      ) . all()

  assert ( len( df[ ( df["estrato"]==9 ) |
                    ( pd.isnull( df["estrato"] ) )
              ] ) <
           ( len(df) / 50 ) )

def test_ranges( bs : pd.DataFrame ) -> None:
  for (c,t) in [
    ("recently bought this house" , cla.InSet( {True,False} ) ),
    ("recently bought this house" , cla.CoversRange( 0,1 ) ),
    ("recently bought this house" , cla.MeanBounds( 0,0.01 ) ),
    ("recently bought this house" , cla.MissingAtMost( 0 ) ),
    ("estrato"                    , cla.InSet( set( range(0,6) ) ) ),
    ("estrato"                    , cla.CoversRange( 0, 3 ) ),
    ("estrato"                    , cla.MeanBounds( 1.5, 2.5 ) ),
    ("estrato"                    , cla.MissingAtMost( 0.02 ) ) ]:
    assert t.test( bs[c] )

if True: # run tests
  log = "starting\n"
  bs = oio.readStage(
      1 # PITFALL: For buildings, we always use the full sample.
    , 'buildings'
    , dtype = {"estrato":'float64'}
      # If subsample is so small that there are no missing values,
      # "estrato" will by default be read as "int64".
  )
  test_types( bs )
  test_nullity( bs )
  test_ranges( bs )
  assert( unique( bs.columns ) )
  oio.test_write( 1 # PITFALL: For buildings, we always use the full sample.
                , "build_buildings"
                , log )
