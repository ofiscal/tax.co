import python.common.util as util
import pandas as pd
import python.build.output_io as oio


if True: # initialize log
  test_output_filename = "build_buildings"
  oio.test_clear( test_output_filename )
  def echo( content ):
    oio.test_write( test_output_filename
                  , content )
  echo( ["starting"] )


def check_types( df ):
  for (c,t) in [ ("household","int64")
               , ("region-1","O")
               , ("region-2","O")
               , ("estrato","float64") ]:
    assert df[c].dtype == t

def check_nullity( df ):
  for c in ["household","region-1","region-2"]:
    assert len( df[ pd.isnull( df[c] ) ] ) == 0
  
  for c in ["region-1","region-2"]:
    # none of these strings should be empty
    assert df[c].apply( lambda x: len(x) > 0 
                      ) . all() 
  
  assert ( len( df[ ( df["estrato"]==9 ) |
                    ( pd.isnull( df["estrato"] ) )
              ] ) <
           ( len(df) / 50 ) )


if True: # run tests
  bs = oio.readStage( 1, 'buildings' )
  check_types( bs )
  check_nullity( bs )
