import numpy as np
import pandas as pd


colDict = { "P6050"      : "relationship" }

ppl = pd.read_csv(
  "data/enph-2017/recip-1/Caracteristicas_generales_personas.csv"
  , usecols = list( colDict.keys() )
  ) . rename( columns = colDict )

ppl[ "child" ] = (
  ( ppl["relationship"] == 3 )     # hijo, hijastro
  | ( ppl["relationship"] == 4 ) ) # nieto

ppl[ "non-child family" ] = (
  ( ppl["relationship"] == 2 )     # Pareja, esposo(a), cónyuge, compañero(a)
  | ( ppl["relationship"] == 5 ) ) # Otro pariente

( len( ppl[ ppl["relationship"] == 3 ] )
  / len(ppl) )
( len( ppl[ ppl["relationship"] == 4 ] )
  / len(ppl) )
( len( ppl[ ppl["child"] == True ] )
  / len(ppl) )

( len( ppl[ ppl["relationship"] == 2 ] )
  / len(ppl) )
( len( ppl[ ppl["relationship"] == 5 ] )
  / len(ppl) )
( len( ppl[ ppl["non-child family"] == True ] )
  / len(ppl) )
