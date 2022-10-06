-- | PURPOSE: This demonstrates an algorithm for allocating dependents.
-- The highest earner takes up to 4 dependents.
-- Then the next takes up to 4.
-- Etc.

test :: Bool
test = and
  [ dependentsToClaim 0 1 == 0
  , dependentsToClaim 0 2 == 0
  , dependentsToClaim 0 3 == 0

  , dependentsToClaim 1 1 == 1
  , dependentsToClaim 1 2 == 0
  , dependentsToClaim 1 3 == 0

  , dependentsToClaim 3 1 == 3
    -- 4 * 1 is only a bit > 3, so get some.
  , dependentsToClaim 3 2 == 0
    -- 4 * 2 = 8 >> 3, so get none.
  , dependentsToClaim 3 3 == 0
    -- 4 * 3 = 8 >> 3, so get none.

  , dependentsToClaim 5 1 == 4
    -- 4 * 1 < 5, so get some.
  , dependentsToClaim 5 2 == 1
    -- 4 * 2 = 8 is only a bit > 5, so get some.
  , dependentsToClaim 5 3 == 0
    -- 4 * 3 = 12 >> 5, so get none.

  , dependentsToClaim 6 1 == 4
  , dependentsToClaim 6 2 == 2
  , dependentsToClaim 6 3 == 0
  , dependentsToClaim 6 4 == 0

  , dependentsToClaim 8 1 == 4
  , dependentsToClaim 8 2 == 4
  , dependentsToClaim 8 3 == 0
  , dependentsToClaim 8 4 == 0
  ]

dependentsToClaim
  :: Int -- ^ number of dependents in the household
  -> Int -- ^ earner's rank (a positive integer) in household
  -> Int -- ^ number of dependents to claim
dependentsToClaim nDeps earnerIncomeRank =
  let x = earnerIncomeRank * 4 - nDeps
  in if x >= 4 then 0
     else if x > 0 then 4 - x
          else 4
