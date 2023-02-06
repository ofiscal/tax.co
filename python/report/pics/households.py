if True:
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
    from functools import reduce
    #
    from   ofiscal_utils.draw.draw import (cdf, single_cdf)
    import python.common.util as util
    import python.draw.util as draw
    import python.build.output_io as oio
    import python.build.common as c


vat_pics_dir = ( "output/vat/pics/recip-" + str(c.subsample) + "/"
               + c.strategy_suffix + "/" )
if not os.path.exists(vat_pics_dir): os.makedirs(vat_pics_dir)
households = oio.readUserData( c.subsample, 'households.' + c.strategy_suffix )
households_decile_summary = oio.readUserData( c.subsample, 'households_decile_summary.' + c.strategy_suffix )


if True: # single series
  plt.close()
  single_cdf( households["members"], "Household size", xmax = 10)
  draw.savefig( vat_pics_dir + "households" , "size" )

  plt.close()
  single_cdf( households["transactions"], "Transactions per month", xmax = 150)
  draw.savefig( vat_pics_dir + "households" , "transactions-per-month" )

  plt.close()
  single_cdf( households["age-min"], "Age of youngest member")
  draw.savefig( vat_pics_dir + "households" , "youngest" )

  plt.close()
  single_cdf( households["age-max"], "Age of oldest member")
  draw.savefig( vat_pics_dir + "households" , "oldest" )


  if True: # household income, logx and linear x
    plt.close()
    single_cdf( households["income"], "Household income",
                xmax = 3e6)
    plt.gca().xaxis.set_major_formatter (
      EngFormatter ( places = 2 ) )
    draw.savefig ( vat_pics_dir + "households" , "income" )

    plt.close()
    single_cdf( households["income"], "Household income",
                xmin = 1e4, # as a monthly income in pesos, that's basically zero
                logx = True)
    draw.savefig( vat_pics_dir + "households/logx" , "income" )

  plt.close()
  plt.title("Highest education level among household members")
  plt.xticks( np.arange(1,10,1),
              [ "Ninguno",
                "Preescolar",
                "Basica\n Primaria",
                "Basica\n Secundaria",
                "Media",
                "Superior o\n Universitaria",
                "(unused\n value)",
                "(unused\n value)",
                "No sabe,\n no informa" ],
              rotation='vertical')
  draw.table( households, "edu-max" )
  draw.savefig( vat_pics_dir + "households" , "max-edu" )


if True: # VAT expenditures by income decile
  # PITFALL: Since 47% of households report zero income, nothing
    # distinguishes the first 5 deciles, so they are grouped together.
    # The "duplicates='drop'" option to pd.qcut achieves that grouping.

  draw.to_latex (
    util.tabulate_min_median_max_by_group (
      households, "income-decile", "income" ),
    "output/vat/tables/recip-" + str(c.subsample),
    "income-by-income-decile",
  )

  draw.to_latex(
    util.tabulate_min_median_max_by_group(
      households, "income-decile", "vat/value, min" ),
    "output/vat/tables/recip-" + str(c.subsample),
    "vat-over-spending,min,-by-income-decile")

  draw.to_latex(
    util.tabulate_min_median_max_by_group( households, "income-decile", "vat/value, max" ),
    "output/vat/tables/recip-" + str(c.subsample),
    "vat-over-spending,max,-by-income-decile")


  if True: # vat / income (left) and vat/value (right) by income decile, both in the same figure
    styles = [":","-"]*5 # ten from the sequence - : - : - ...
    colors = reduce( lambda x,y: x+y # ten from the sequence red, red, orange, orange, ...
                     , [ [x,x] for x in ["red","orange","yellow","green","blue"] ] )

    if True: # minimum VAT possible
      plt.close()

      plt.suptitle("CDFs of VAT expenditure across households by income decile")

      plt.subplot(1,2,1)
      plt.xlabel("VAT paid / value consumed")
      plt.ylabel("Probability")
      for i in list(households_decile_summary.index):
        cdf( households                           \
             [ households["income-decile"]==i ] \
             ["vat / income, min"],
             linestyle = styles[i],
             color = colors[i],
             xmax = 0.1,
             with_mean = False,
            )
      plt.grid(color='b', linestyle=':', linewidth=0.5)

      plt.subplot(1,2,2)
      plt.ylabel("Probability")
      for i in list(households_decile_summary.index):
        cdf( households                           \
                    [ households["income-decile"]==i ] \
                    ["vat/value, min"],
                  linestyle = styles[i],
                  color = colors[i],
                  xmax = 0.1,
                  with_mean = False
        )
      plt.grid(color='b', linestyle=':', linewidth=0.5)

      ax = plt.gca()
      ax.set_yticklabels([])

      fig = plt.gcf()
      fig.set_size_inches(8,4)

      draw.savefig(vat_pics_dir + "households", "VAT-over-consumption,-by-income-decile.png")


    if True: # maximum VAT possible
      plt.close()

      plt.suptitle("CDFs of VAT expenditure across households by income decile")

      plt.subplot(1,2,1)
      plt.xlabel("VAT paid / value consumed")
      plt.ylabel("Probability")
      for i in list(households_decile_summary.index):
        cdf( households                           \
                    [ households["income-decile"]==i ] \
                    ["vat / income, max"],
                  linestyle = styles[i],
                  color = colors[i],
                  xmax = 0.1,
                  with_mean = False
        )
      plt.grid(color='b', linestyle=':', linewidth=0.5)

      plt.subplot(1,2,2)
      plt.ylabel("Probability")
      for i in list(households_decile_summary.index):
        cdf( households                           \
                    [ households["income-decile"]==i ] \
                    ["vat/value, max"],
                  linestyle = styles[i],
                  color = colors[i],
                  xmax = 0.1,
                  with_mean = False
        )
      plt.grid(color='b', linestyle=':', linewidth=0.5)

      ax = plt.gca()
      ax.set_yticklabels([])

      fig = plt.gcf()
      fig.set_size_inches(8,4)

      draw.savefig(
        vat_pics_dir + "households",
        "VAT-over-consumption,-by-income-decile.png")
