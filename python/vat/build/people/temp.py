import python.vat.build.main as data
import python.vat.build.people.files as files
import python.util as util
import pandas as pd

people["beca sources, govt"]    = people[ list( files.beca_govt   .values() ) ].sum()
people["beca sources, private"] = people[ list( files.beca_private.values() ) ].sum()

util.describeWithMissing( data.people[ ["beca sources, govt"] + list( files.beca_govt.values() ) ] )
util.describeWithMissing( data.people[ ["beca sources, private"] + list( files.beca_private.values() ) ] )

df = pd.DataFrame( [[1,2],[3,4]], columns = ["a","b"] )
df["c"] = df.sum()
 
