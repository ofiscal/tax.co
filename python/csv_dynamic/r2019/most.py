from python.common.misc import muvt


def f(x):
  return ( (x - 0.0 * muvt)*0.0 + 0.0*muvt if x < (1090.0*muvt)
  else ( (x - 1090.0 * muvt)*0.19 + 0.0*muvt if x < (1700.0*muvt)
  else ( (x - 1700.0 * muvt)*0.28 + 115.9*muvt if x < (4100.0*muvt)
  else ( (x - 4100.0 * muvt)*0.33 + 787.9*muvt if x < (8670.0*muvt)
  else ( (x - 8670.0 * muvt)*0.35 + 2296.0*muvt if x < (18970.0*muvt)
  else ( (x - 18970.0 * muvt)*0.37 + 5901.0*muvt if x < (31000.0*muvt)
  else ( (x - 31000.0 * muvt)*0.39 + 10352.1*muvt 
  )))))))
