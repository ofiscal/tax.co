import sys
import pandas                    as pd
import numpy as np

%matplotlib inline
  # enable the previous line if calling from Jupyter
import matplotlib
# matplotlib.use('Agg')
  # enable the previous line if calling from the (non-gui) shell
import matplotlib.pyplot as plt

import python.build.output_io    as oio
import python.common.util               as util
import python.common.misc as c
import python.common.cl_args as c
import python.build.ss_functions as ss


xs = pd.Series( np.arange( 0, 30e6, 0.5e6 ) )
for (title, compute) in [ 
      ("tax, pension"               , ss.mk_pension)
    , ("tax, pension, employer"     , ss.mk_pension_employer)
    , ("tax, salud"                 , ss.mk_salud)
    , ("tax, salud, employer"       , ss.mk_salud_employer)
    , ("tax, solidaridad"           , ss.mk_solidaridad)
    , ("tax, parafiscales"          , ss.mk_parafiscales_employer)
    , ("tax, cajas de compensacion" , ss.mk_cajas_de_compensacion_employer)
    , ("cesantias + primas"         , ss.mk_cesantias_employer) ]:
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.set_title(title + ", asalariados")
  ys = xs.apply( lambda wage: compute( 0, wage ) )
  ax = fig.add_subplot(111)
  ax.set_xlabel("wage")
  ax.set_ylabel("contribution")
  plt.plot( xs, ys )

  fig = plt.figure()  
  ax = fig.add_subplot(111)
  ax.set_title(title + ", independientes")
  ys = xs.apply( lambda wage: compute( 1, wage ) )
  ax = fig.add_subplot(111)
  ax.set_xlabel("wage")
  ax.set_ylabel("contribution")
  plt.plot( xs, ys )
