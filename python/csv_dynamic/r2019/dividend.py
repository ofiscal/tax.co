from python.common.misc import muvt


def f(x):
  return ( (x - 0.0 * muvt)*0.0 + 0.0*muvt if x < (300.0*muvt)
  else ( (x - 300.0 * muvt)*0.1 + 0.0*muvt
  ))
