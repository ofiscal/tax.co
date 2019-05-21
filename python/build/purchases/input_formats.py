# input files
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
import python.build.input_formats as ifo


def test_purchase_inputs():
  for f in articulos.files:
    df = cl.retrieve_file( f )
    acc = {}
    for c in df.columns:
      acc.update( [ (c, ifo.varContentFormats( df[c] ) ) ] )
      assert acc[c] == cla.input_map( f.col_specs )[c]
