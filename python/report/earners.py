if True:
  import pandas as pd
  import numpy as np
  #
  import python.build.output_io as oio
  import python.common.common as com


earners = oio.readStage(
  com.subsample,
  "people_4_post_households." + com.strategy_year_suffix )

fake = pd.DataFrame ( { "fake 1" : [1,2],
                        "fake 2" : [2,3], } )

oio.saveStage(
    com.subsample,
    fake,
    "report_earners_tmi." + com.strategy_year_suffix )
oio.saveStage_excel(
    com.subsample,
    fake,
    "report_earners_tmi." + com.strategy_year_suffix )
oio.saveStage(
    com.subsample,
    fake,
    "report_earners." + com.strategy_year_suffix )
oio.saveStage_excel(
    com.subsample,
    fake,
    "report_earners." + com.strategy_year_suffix )
