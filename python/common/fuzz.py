import numpy  as np
import pandas as pd


def fuzz_peso_values ( s : pd.Series ) -> pd.Series:
  """Add a negligible amount to a peso-denominated value.
  Since pesos are of so little value,
  adding a random value between 0 and 1 pesos
  should not make any meaningful difference
  (but it allows quantiles to be of the same size).
  However, that random value has to be bigger
  if it's being added to something very big,
  in order not be lost due to floating point error.
  """
  return s.apply (
    lambda x: ( x
                + max ( 1, x * 1e-5 )
                * np.random.random() ) )
