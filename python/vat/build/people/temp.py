import python.vat.build.main as data
import python.vat.build.people.files as files
import python.util as util

data.people["beca govt"] = data.people[ list( files.beca_govt.values() ) ].sum()
data.people["beca private"] = data.people[ list( files.beca_private.values() ) ].sum()

util.describeWithMissing( data.people[ ["beca govt"] + list( files.beca_govt.values() ) ] )
util.describeWithMissing( data.people[ ["beca private"] + list( files.beca_private.values() ) ] )

df = pd.DataFrame( [[1,2],[3,4]], columns = ["a","b"] )
