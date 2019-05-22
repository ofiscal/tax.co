import sys
sys.path.insert(0, '.') # assuming pytest is run from the top of the project, this
                        # allows local ("python.something.something") imports to work
import python.build.classes as cla
import python.common.cl_args as cl
import python.build.output_io as oio
import python.build.purchases.nice_purchases as nice_purchases
import python.build.purchases.medios as medios
import python.build.purchases.articulos as articulos
import python.build.purchases.capitulo_c as capitulo_c


test_output_filename = "purchase_input_formats"

oio.test_clear( test_output_filename )
def echo( content ):
  oio.test_write( test_output_filename
                , content )

def test_purchase_inputs():
  for f in (
      articulos.files
#         # + medios.files
#           + capitulo_c.files
#           + nice_purchases.files
           ): 
    df = cl.retrieve_file( f )
    acc = {}
    for c in df.columns:
      echo( [f.name, c] )
      acc.update( [ (c, cla.stringProperties( df[c] ) ) ] )
      assert acc[c] == cla.input_map( f.col_specs )[c]

test_purchase_inputs()