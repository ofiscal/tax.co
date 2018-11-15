import pandas as pd
import python.build.datafiles as datafiles
import os as os

for (survey,year) in [("enig",2007),("enph",2017)]:
  outputFolder = "output/summary/" + survey + "-" + str(year) + "/recip-100/"
  if not os.path.exists(outputFolder): # this disregards a race condition that
    # could appear if multiple processes were building folders; see
    # https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
    os.makedirs(outputFolder)

  for filename in datafiles.files[year]:
    print("now processing: " + filename)
    dest = open( outputFolder + filename + ".txt"
                , "w+")
    dest.write("\n\ndataset: " + filename)
    df = pd.read_csv( datafiles.yearSurveyFolder(year) + "recip-100/"
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
    dest.close()
