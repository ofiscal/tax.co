import sys
import python.build.classes as cla
import python.common.cl_args as cl
import python.build.output_io as oio
import python.build.purchases.nice_purchases as nice_purchases
import python.build.purchases.medios as medios
import python.build.purchases.articulos as articulos
import python.build.purchases.capitulo_c as capitulo_c


if True: # initialize log
  test_output_filename = "purchase_inputs"
  oio.test_clear( cl.subsample
                , test_output_filename )
  def echo( content ):
    oio.test_write( cl.subsample
                  , test_output_filename
                  , content )
  echo( ["starting"] )


def test_purchase_inputs():
  for f in ( articulos.files
         # + medios.files
           + capitulo_c.files
           + nice_purchases.files
           ): 
    df = cl.retrieve_file( f )
    acc = {}
    for c in df.columns:
      echo( [f.name, c] )
      acc.update( [ (c, cla.stringProperties( df[c] ) ) ] )
      assert acc[c] == cla.input_map( f.col_specs )[c]


if True: # run tests
  test_purchase_inputs()
