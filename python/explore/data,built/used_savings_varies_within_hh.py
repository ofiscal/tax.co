if True:
  import pandas as pd
  import python.build.output_io as oio
  import python.common.common as com

ppl = oio.readStage(com.subsample, 'people_1')
dp = ppl[["household","used savings"]].copy()
dp["one"] = 1
dh = ( dp . groupby("household")
          . agg("sum") )
