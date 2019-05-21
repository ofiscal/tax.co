import python.common.cl_args as cl
import python.build.output_io as oio

# input files
import sys
sys.path.insert(0, '.') # assuming pytest is run from the top of the project, this
                        # allows local ("python.something.something") imports to work
import python.build.purchases.nice_purchases as nice_purchases
import python.build.purchases.medios as medios
import python.build.purchases.articulos as articulos
import python.build.purchases.capitulo_c as capitulo_c
import python.build.input_formats as ifo


x = cl.retrieve_file( articulos.files[0] )
acc = {}
for c in x.columns:
  acc.update( [ (c, ifo.varContentFormats( x[c] ) ) ] )
