import numpy as np
import python.vat.build.people.files as files
import python.vat.build.common as common
import python.util as util
import pandas as pd


people = common.collect_files( files.files )

people["non-beca sources"].unique()
people["P6236"].unique()


people = pd.read_csv(
         "data/enph-2017/recip-100/Caracteristicas_generales_personas.csv"
         , usecols = ["P6236"]
#        , dtype = { "P6236" : 'O'
#                  , "non-beca sources" : 'O' }
)
people["P6236"].unique()





import python.vat.build.main as data


people["beca sources, govt"]    = people[ list( files.beca_govt   .values() ) ].sum()
people["beca sources, private"] = people[ list( files.beca_private.values() ) ].sum()

util.describeWithMissing( data.people[ ["beca sources, govt"] + list( files.beca_govt.values() ) ] )
util.describeWithMissing( data.people[ ["beca sources, private"] + list( files.beca_private.values() ) ] )

df = pd.DataFrame( [[1,2],[3,4]], columns = ["a","b"] )
df["c"] = df.sum()

## something else 
df = pd.DataFrame( [" 1 3 5 ", "" ], columns = ["a"] )
df["b"] = df["a"].apply( files.count_public )
df["c"] = df["a"].apply( files.count_private )
