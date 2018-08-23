# I used this to look for a correspondence between files in the pre-release and official versions of the ENPH.
# I discovered that there isn't (a very close) one.

import pandas as pd
import python.enph_compare_official_to_pre_release.files as filetree


acc = []

for f in filetree.old_files:
  df = pd.read_csv( filetree.old_folder + f + ".csv" )
  cols = list(df.columns)
  acc.append( ( len(cols)
              , f + str(cols) + "\n" ) )

for f in filetree.new_files:
  df = pd.read_csv( filetree.new_folder + f + ".csv" )
  cols = list(df.columns)
  acc.append( ( len(cols)
              , f + str(cols) + "\n" ) )

acc2 = sorted(acc, key = lambda x: x[0])

target = open( filetree.output_folder + "file-columns.txt"
             , "w+")
for x in acc2:
  target.write( (str(x[0]) + " " + x[1] + "\n")
                .lower() )
target.close()
