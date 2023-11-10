if True:
  import matplotlib
  import matplotlib.pyplot as plt
  import pandas                  as pd
  from   scipy import stats
  #
  from   ofiscal_utils.draw.draw import (cdf, single_cdf)
  import python.build.output_io  as oio
  import python.common.common    as com
  import python.draw.util        as draw


if True: # load data
  households = oio.readUserData(
      com.subsample,
      "households_2_purchases." + com.strategy_year_suffix )

  earners = oio.readUserData(
      com.subsample,
      "people_4_earners_post_households." + com.strategy_year_suffix )

ei = earners["income"]
ei[ ei > ei.quantile(0.99) ]

for name, bottom in [ ("all", 0),
                      ("top-half",0.5),
                      ("top-tenth",0.9),
                      ("top-percent",0.99) ]:
  cdf ( ei[ ei > ei.quantile(bottom) ],
        logx = True,
        with_mean = True )
  draw.savefig( "zoom-in-on-rich",
                name + ".jpg" )
  plt.close()
