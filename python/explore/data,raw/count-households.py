if True:
  import numpy as np
  import pandas as pd
  import python.common.misc as c
  import python.common.common as cl
  import python.common.util as util

colDict = { "DIRECTORIO" : "household"
}

ppl = pd.read_csv(
  "data/enph-2017/recip-1"
  + "/Caracteristicas_generales_personas.csv"
  , usecols = list( colDict.keys() )
  ) . rename( columns = colDict )

len( ppl["household"].unique() )
