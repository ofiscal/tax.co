# Extract the unique values in every non-numeric field of every data set.
# Write to a file tree the leaves of which correspond to columns.

import pandas as pd
import python.datafiles as datafiles
import os as os

for (survey,year) in [("enig",2007),("enph",2017)]:
  for filename in datafiles.files[year]:
    print("now processing: year " + str(year) + ", file " + filename)
    df = pd.read_csv( datafiles.folder(year) + "recip-1/"
                      + filename + ".csv")
    outputFolder = "output/string-columns/" + survey + "-" + str(year) + "/" + filename

    for colname in list(df.columns.values):
      if not os.path.exists(outputFolder): # this disregards a race condition that
        # could appear if multiple processes were building folders; see
        # https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
        os.makedirs(outputFolder)
      col = df[colname]
      if col.dtype == object:
        dest = open(outputFolder + "/" + colname
                    , "w+")
        dest.write( "\n".join(
          [ str(y) for y in col.unique().tolist() ]
        ) )
        dest.close()
