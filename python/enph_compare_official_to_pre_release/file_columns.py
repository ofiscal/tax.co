import pandas as pd
import python.enph_compare_official_to_pre_release.files


acc = []

for f in old_files:
  df = pd.read_csv(old_folder + f + ".csv")
  cols = list(df.columns)
  acc.append( ( len(cols)
              , f + str(cols) + "\n" ) )

for f in new_files:
  df = pd.read_csv(new_folder + f + ".csv")
  cols = list(df.columns)
  acc.append( ( len(cols)
              , f + str(cols) + "\n" ) )

acc2 = sorted(acc, key = lambda x: x[0])

target = open( output_folder + "file-columns.txt",
             , "w+")
for x in acc2:
  target.write( (str(x[0]) + " " + x[1] + "\n")
                .lower() )
target.close()
