import pandas as pd


# Determine dependents, for income tax, assuming rationality -- that is,
# the highest earner should claim the first available dependent,
# the next-highest earner should claim the next available dependent, etc.
def insert_has_dependent_column( df : pd.DataFrame ) -> pd.DataFrame:
  hh = ( df[["household","dependent"]]
       . groupby( "household" )
       . agg( 'sum' )
       . rename( columns = {"dependent":"dependents"} )
       . reset_index() )
  df = ( df.merge( hh, how='inner', on='household' )
        . drop( columns = "dependent" ) )
  df["has dependent"] = (
    df["member-by-income"] <= df["dependents"] )
  return df

