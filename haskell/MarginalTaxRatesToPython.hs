{-# LANGUAGE MultiWayIf
, ScopedTypeVariables
, TypeApplications
#-}

module MarginalTaxRatesToPython where

import Data.List (takeWhile)
import Data.List.Split (splitOn)


-- ** Types

-- | A way to represent marginal tax rates.
data MoneyBracket = MoneyBracket
  { top :: Float
  , rate :: Float } deriving (Show)

-- | A formula from money (usually income, sometimes wealth)
-- to total (not marginal) tax owed.
data Formula = Formula
  { fSubtract :: Float
  , fRate :: Float
  , fAdd :: Float
  , fMax :: Float }

instance Show Formula where
  show f = "(x - " ++ show (fSubtract f) ++ " * muvt)*" ++
           show (fRate f) ++ " + " ++ show (fAdd f)
           ++ "*muvt if x < (" ++ show (fMax f) ++ "*muvt)"


-- ** Formatting the math.

-- * The first, worse idiom.
-- This was designed to be run from ghci; then I would copy, paste
-- and format the resulting pythong code by hand.

-- | PITFALL: This name sucks, but alas it is highly referred to,
-- by programs that are not part of this cabal package.
-- (If they were part of it I could just change the name and see in GHCI
-- which references had broken.)
go :: Formula -> [MoneyBracket] -> IO ()
go initialFormula brackets =
  mapM_ (putStrLn . show) $
  scanl unMarginalize initialFormula brackets


-- * The later, better idiom.

formulasToPython :: [Formula] -> [String]
formulasToPython fs =
  "def f(x):" : ( map ("  " ++) $
                  wrapConditions $
                  dropLastCondition $
                  map show fs )

wrapConditions :: [String] -> [String]
wrapConditions (s:ss) = let
  s' = "return ( " ++ s
  ss' = map ("else ( " ++) ss
  cap = replicate (length $ s:ss) ')'
  in s' : ss' ++ [cap]

-- | The last tax rate has no ceiling, so the "if x < _" condition
-- does not apply. Moreover it *must* be dropped in order to be valid Python;
-- otherwise it would be missing another "else" clause.
--
-- PITFALL: This hack only happens to work because the letter "i"
-- does not appear before the word "if" in the formulas constructed by
-- `bracketsToFormulas`.
dropLastCondition :: [String] -> [String]
dropLastCondition ss =
  let last:earlier = reverse ss
  in reverse (takeWhile (/= 'i') last : earlier)


-- ** The math, if it can be called that.

bracketsToFormulas :: [MoneyBracket] -> [Formula]
bracketsToFormulas bs = let
  f0 = initialFormula $ head bs
  in scanl unMarginalize f0 $ tail bs

-- | The formula that applies to the taxpayers with the least money to tax.
initialFormula :: MoneyBracket -> Formula
initialFormula b = Formula 0 (rate b) 0 (top b)

unMarginalize :: Formula -> MoneyBracket -> Formula
unMarginalize prev bracket =
  Formula { fSubtract = fMax prev
          , fRate = rate bracket
          , fAdd = fAdd prev +
                   fRate prev * (fMax prev - fSubtract prev)
          , fMax = top bracket }


-- ** Inputx CSV data

type Table = ([String],[[Float]])

-- | PITFALL: Needs to be used to validate the marginal tax rates,
-- but not the VAT rates, as those get validated by Python, in
-- python/build/rate_input_test.py
validateTable :: [String] -> [(Float,Float)] -> Table
              -> Either String ()
validateTable names bounds (names', rows) =
  mapLeft (++ "validateTable: ") $
  let validateRowBounds :: ((Float,Float), [Float]) -> Bool
      validateRowBounds ((low,high), fs) = and (map (>= low) fs)
                                        && and (map (<= high) fs)
      validateRowLength :: [Float] -> Bool
      validateRowLength fs = length fs == length names
  in if | names /= names' -> Left $ "Observed columns " ++ show names'
          ++ " not equal to expected columns " ++ show names ++ "."
        | not $ and $ map validateRowLength rows -> Left $
          "Rows of table should all have length " ++ show (length names)
          ++ " but do not."
        | not $ and $ map validateRowBounds $ zip bounds rows -> Left $
          "Table cells out of bounds."
        | otherwise -> Right ()

csvToTable :: String -> IO Table
csvToTable filename = do
  (columnNames : rows) :: [[String]] <-
    map (splitOn ",") . lines
    <$> readFile filename
  return (columnNames, map (map $ read @Float) rows)


-- ** Utilities

-- | This could be imported from Data.Either.Combinators,
-- if I installed that. (`cabal update`, `cabal install either`).
-- But it seems substantial.
mapLeft :: (a -> b) -> Either a c -> Either b c
mapLeft f (Left a) = Left $ f a
mapLeft _ (Right c) = Right c
