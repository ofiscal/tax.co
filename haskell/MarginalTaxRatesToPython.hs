module MarginalTaxRatesToPython where

import Data.List (takeWhile)

-- * Types

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


-- | The first idiom.
-- The initial formula describes the first tax rate.
-- I'm not sure why I thought I needed to do that.
-- This was designed to be run from ghci; then I would copy, paste
-- and format the resulting pythong code by hand.
--
-- PITFALL: This name sucks, but alas it is highly referred to,
-- by programs that are not part of this cabal package.
-- (If they were part of it I could just change the name and see in GHCI
-- which references had broken.)
go :: Formula -> [MoneyBracket] -> IO ()
go initialFormula brackets =
  mapM_ (putStrLn . show) $
  scanl unMarginalize initialFormula brackets

-- | PITFALL: This hack only happens to work because the letter "i"
-- only shows up in the word "if" in the formulas constructed by
-- `bracketsToFormulas`.
dropLastCondition :: [String] -> [String]
dropLastCondition ss =
  let last:earlier = reverse ss
  in reverse (takeWhile (/= 'i') last : earlier)

bracketsToFormulas :: [MoneyBracket] -> [Formula]
bracketsToFormulas bs = let
  f0 = initialFormula $ head bs
  in scanl unMarginalize f0 $ tail bs

initialFormula :: MoneyBracket -> Formula
initialFormula b = Formula 0 (rate b) 0 (top b)

unMarginalize :: Formula -> MoneyBracket -> Formula
unMarginalize prev bracket =
  Formula { fSubtract = fMax prev
          , fRate = rate bracket
          , fAdd = fAdd prev +
                   fRate prev * (fMax prev - fSubtract prev)
          , fMax = top bracket }
