import pandas as pd


def dependentsToClaim (
    nDeps            : int, # number of dependents in the household
    earnerIncomeRank : int  # earner's rank (a positive integer) in household
) -> int:
  x = earnerIncomeRank * 4 - nDeps
  return ( 0
           if x >= 4
           else ( 4 - x
                  if x > 0
                  else 4 ) )

def test_dependentsToClaim ():
  # TODO: Incorporate into tests in Makefile.
  assert dependentsToClaim( 0, 1 ) == 0
  assert dependentsToClaim( 0, 2 ) == 0
  assert dependentsToClaim( 0, 3 ) == 0

  assert dependentsToClaim( 1, 1 ) == 1
  assert dependentsToClaim( 1, 2 ) == 0
  assert dependentsToClaim( 1, 3 ) == 0

  assert dependentsToClaim( 3, 1 ) == 3
    # 4 * 1 is only a bit > 3, so get some.
  assert dependentsToClaim( 3, 2 ) == 0
    # 4 * 2 = 8 >> 3, so get none.
  assert dependentsToClaim( 3, 3 ) == 0
    # 4 * 3 = 8 >> 3, so get none.

  assert dependentsToClaim( 5, 1 ) == 4
    # 4 * 1 < 5, so get some.
  assert dependentsToClaim( 5, 2 ) == 1
    # 4 * 2 = 8 is only a bit > 5, so get some.
  assert dependentsToClaim( 5, 3 ) == 0
    # 4 * 3 = 12 >> 5, so get none.

  assert dependentsToClaim( 6, 1 ) == 4
  assert dependentsToClaim( 6, 2 ) == 2
  assert dependentsToClaim( 6, 3 ) == 0
  assert dependentsToClaim( 6, 4 ) == 0

  assert dependentsToClaim( 8, 1 ) == 4
  assert dependentsToClaim( 8, 2 ) == 4
  assert dependentsToClaim( 8, 3 ) == 0
  assert dependentsToClaim( 8, 4 ) == 0

# Determine dependents, for income tax, assuming rationality -- that is,
# the highest earner should claim the first available dependent,
# the next-highest earner should claim the next available dependent, etc.
def insert_claims_dependents_columns (
    df : pd.DataFrame # Should have "household", "dependent" (bool),
                      # and "rank, labor income".
)     -> pd.DataFrame: # Just like the input, except:
  # It will have two columns for claiming depenents:
  # "claims dependent (labor income tax)", which is a bool,
  # and corresponds to the status quo as of May 2022, and
  # "dependents to claim (up to 4)", which gives a number in [0,4],
  # and corresponds to a proposal being mooted as of Oct 6 2022.
  hh = ( df[["household","dependent"]]
       . groupby( "household" )
       . agg( 'sum' )
       . rename( columns = {"dependent":"dependents"} )
       . reset_index() )
  df = df.merge( hh, how='inner', on='household' )
  df["claims dependent (labor income tax)"] = (
    df["rank, labor income"] <= df["dependents"] )
  df["dependents to claim (up to 4)"] = df.apply (
    lambda row: dependentsToClaim (
      nDeps            = row["dependents"],
      earnerIncomeRank = row["rank, labor income"] ),
    axis = 1 )
  return df
