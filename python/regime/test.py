# TODO : This folder of code is so complicated,
# and the functions in it so long,
# that testing is difficult, and so far hasn't happened.

if True:
  import pandas                                 as pd
  #
  import python.build.output_io                 as oio
  import python.common.common                   as com
  from   python.common.misc import muvt
  import python.regime.cedula_general_gravable  as cgg


def example_test():
  assert True

example_test()

oio.test_write (
    com.subsample,
    "python_regime_test",
    "It worked." )
