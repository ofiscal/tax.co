# Count households, household members.
# Verify that DIRECTORIO probably means household,
# and that in the person data,
# ORDEN is probably a unique-within-household person ID.

if True:
  from typing import List
  import numpy as np
  import pandas as pd
  import python.common.misc as c
  import python.common.common as cl
  import python.common.util as util


colDict = {
  "DIRECTORIO" : "hh",
  "ORDEN"      : "mbr",
  "P6020"      : "female",
  "P6040"      : "age",
}

ppl = pd.read_csv(
  "data/enph-2017/recip-1"
  + "/Caracteristicas_generales_personas.csv"
  , usecols = list( colDict.keys() )
  ) . rename( columns = colDict )

hh = ( ppl . groupby( "hh" )
      . agg( {"mbr" : "max" } )
      . reset_index()
      . rename( columns = {"mbr" : "mbr, max"} ) )

d = pd.DataFrame( {"x" : [1,1,1],
                   "y" : [1,2,2]} )

ppl_dup_check = ppl.copy()
ppl_dup_check["age"] = str(ppl_dup_check["hh"])

if False: # This idiom turns out to run glacially slowly.
  def has_dup( df : pd.DataFrame,
               cols : List[str]
             ) -> pd.DataFrame:
      return pd.DataFrame( {
          "hh" : df["hh"],
          "has dup" :  df[cols].duplicated().max() } )
  if True: # test it
      # The first household has no duplicates, the second does.
      ( pd.DataFrame( {"hh"     : [1,1,1,1, 2,2,2,2],
                       "age"    : [0,1,0,1, 0,1,1,1],
                       "female" : [0,0,1,1, 0,0,1,1] } )
       . groupby( "hh" )
       . apply( lambda df: has_dup( df, ["age","female"] ) )
       . groupby( "hh" ) # TODO ? this should not require a second step
       . agg( {"has dup" : "max"} )
       . reset_index()
       . equals( pd.DataFrame( {"hh" : [1,2],
                                "has dup" : [False,True] } ) ) )
  if True: # I've broken this into two steps because the first takes forever.
    ppl_dup = (  ppl.groupby( "hh" )
               . apply( lambda df:
                        has_dup( df, ["age","female"] ) ) )
    ppl_dup = ( ppl_dup
              . groupby( "hh" )
              . agg( {"has dup" : "max"} )
              . reset_index() )
  ppl_dup["has dup"].describe()
    # mean is 1.7%. That's good -- only 1.7% of households have two rows
    # with the same age and gender. This suggests that it is in fact a unique
    # (within household) household member id.

hhm = ( ppl . groupby( ["hh", "mbr"] )
      . agg( # I don't care about this but .agg() wants something
             {"age" : "max"} )
      . reset_index() )

# (hh,mbr) shows no duplicates
len( ppl ) == len( hhm )

# mbr looks like we'd expect if it means household member
ppl = ppl.merge( hh, on="hh" )
ppl["mbr"].min()
hh["mbr, max"].describe()

