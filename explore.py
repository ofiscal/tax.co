import pandas as pd
import datafiles

dest = open("output/summaries.txt", "w+")
for year in [2007,2017]:
  for filename in datafiles.files[year]:
    dest.write("\n\ndataset: " + filename)
    df = pd.read_csv( datafiles.folder(year) + "recip-100/"
                      + filename + ".csv")
    for colname in list(df.columns.values):
      dest.write("\n\n\t" + colname)
      col = df[colname]
      dest.write("\n\t" + "missing: " + str(len(col.index)-col.count()) )
      if col.dtype == object:
        # bounding unique() list with "\n" so it is easily skipped if long
        dest.write("\n\n\t" + str(col.unique()) + "\n")
      else:
        description = map(lambda x: '\t' + x
                          , str(col.describe()).split('\n') )
        dest.write("\n" + "\n".join(description))
