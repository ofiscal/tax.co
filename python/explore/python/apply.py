import pandas as py

df = pd.DataFrame( { "a" : [1,2,3]
                   , "b" : [4,5,6] } )
df.apply( lambda row: row["a"] / row["b"]
        , axis="columns" )
