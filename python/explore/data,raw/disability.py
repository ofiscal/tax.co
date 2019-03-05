import numpy as np
import pandas as pd


colDict = { "P6310" : "why not working" }

ppl = pd.read_csv(
  "data/enph-2017/recip-1/Caracteristicas_generales_personas.csv"
  , usecols = list( colDict.keys() )
  ) . rename( columns = colDict )

# Very few people report wanting to work but not looking for it due to health issues.
( len( ppl[ ppl["why not working"] == '11' ] )
  / len(ppl) )
