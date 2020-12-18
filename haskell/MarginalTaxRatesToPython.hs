module MarginalTaxRatesToPython where

import Data.List (takeWhile)


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

formatFormulas :: [Formula] -> [String]
formatFormulas fs =
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
-- only shows up in the word "if" in the formulas constructed by
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
