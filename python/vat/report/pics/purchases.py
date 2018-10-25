if True: # matplotlib imports are sensitive to order
  # %matplotlib inline
    # enable the previous line if calling from Jupyter
  import matplotlib
  matplotlib.use('Agg')
    # enable the previous line if calling from the (non-gui) shell
  import matplotlib.pyplot as plt
  from matplotlib.ticker import EngFormatter

if True: # more imports
  import sys
  import os
  import numpy as np
  
  import python.vat.build.output_io as oio
  import python.draw.util as draw
  import python.vat.build.common as common


vat_pics_dir = "output/vat/pics/recip-" + str(common.subsample) + "/"
if not os.path.exists(vat_pics_dir): os.makedirs(vat_pics_dir)
purchases = oio.readStage( common.subsample, 'purchases_2_vat')


if True: # purchase quantity, logx and linear
  plt.close()
  draw.single_cdf( purchases["quantity"], "CDF of quantity per purchase",
                   xmin = 1, xmax = 1e3)
  plt.gca().xaxis.set_major_formatter(EngFormatter(places=2))
  draw.savefig( vat_pics_dir + "purchases" , "quantity" )

  plt.close()
  draw.single_cdf( purchases["quantity"], "CDF of quantity per purchase",
                  xmin = 1, logx = True)
  draw.savefig( vat_pics_dir + "purchases/logx" , "quantity" )


if True: # purchase frequency
  plt.close()
  plt.title("Purchase frequency")
  plt.xticks( np.arange(1,12,1),
              ["Diario"
               , "\"Varias veces\n por semana\""
               , "Semanal"
               , "Quincenal"
               , "Mensual"
               , "Bimestral"
               , "Trimestral"
               , "Anual"
               , "\"Esporádico\""
               , "Semestral"
               , "Nunca" ],
              rotation='vertical')
  draw.table( purchases, "freq-code" )
  draw.savefig( vat_pics_dir + "purchases" , "frequency" )


if True: # purchase value, logx and linear
  plt.close()
  draw.single_cdf( purchases["value"], "CDF of monthly purchase value",
                   xmin=1, xmax=1e5)
  plt.gca().xaxis.set_major_formatter(EngFormatter(places=2))
  draw.savefig( vat_pics_dir + "purchases" , "value" )

  plt.close()
  draw.single_cdf( purchases["value"], "CDF of monthly purchase value",
                   xmin =1, logx = True)
  draw.savefig( vat_pics_dir + "purchases/logx" , "value" )


if True: # VAT per purchase, min and max, logx and linear
  plt.close()
  draw.single_cdf( purchases["vat paid, min"], "CDF of min VAT paid per purchase",
                   xmin = 1, xmax = 1e4)
  plt.gca().xaxis.set_major_formatter(EngFormatter(places=2))
  draw.savefig( vat_pics_dir + "purchases" , "vat-in-pesos,min" )

  plt.close()
  draw.single_cdf( purchases["vat paid, min"], "CDF of min VAT paid per purchase",
                   xmin = 0.01, logx = True)
  draw.savefig( vat_pics_dir + "purchases/logx" , "vat-in-pesos,min" )

  plt.close()
  draw.single_cdf( purchases["vat paid, max"], "CDF of max VAT paid per purchase",
                   xmin = 1, xmax = 1e4)
  plt.gca().xaxis.set_major_formatter(EngFormatter(places=2))
  draw.savefig( vat_pics_dir + "purchases" , "vat-in-pesos,max" )

  plt.close()
  draw.single_cdf( purchases["vat paid, max"], "CDF of max VAT paid per purchase",
                   xmin = 0.01, logx = True)
  draw.savefig( vat_pics_dir + "purchases/logx" , "vat-in-pesos,max" )
