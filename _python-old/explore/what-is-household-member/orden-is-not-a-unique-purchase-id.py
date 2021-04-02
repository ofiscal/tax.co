# This code demonstrates that there are duplications -- within almost every purchase file, there appear multiple instances of the same (directorio, orden) pair. Therefore orden cannot be a unique-within-household purchase identifier.


if True:
  from typing import List
  import pandas as pd
  #  
  import python.common.common as com
    # def retrieve_file( file_struct, subsample ):
  import python.build.purchases.nice_purchases as p1
  import python.build.purchases.articulos      as p2
  import python.build.purchases.capitulo_c     as p3


if True:
  def are_uniq( df : pd.DataFrame,
                cols : List[str] ) -> bool:
    m = df.groupby( cols )
    return len(m) == len(df)
  if True: # test it
    x = pd.DataFrame( { "x" : [1,1,2,2],
                        "y" : [1,2,1,2] } )
    assert are_uniq( x, ["x"] ) == False
    assert are_uniq( x, ["x","y"] ) == True

file_structs = p1.files + p2.files + p3.files
files = dict()
for f in file_structs:
  files[ f.filename ] = com.retrieve_file( f, 1 )

for (k,v) in files.items():
  print( k, ": ",
         are_uniq(v, ["DIRECTORIO","ORDEN"] ) )

