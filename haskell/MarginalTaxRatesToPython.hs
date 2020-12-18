module MarginalTaxRatesToPython where


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
go :: Formula -> [MoneyBracket] -> IO ()
go initialFormula brackets =
  mapM_ (putStrLn . show) $
  scanl unMarginalize initialFormula brackets


unMarginalize :: Formula -> MoneyBracket -> Formula
unMarginalize prev bracket =
  Formula { fSubtract = fMax prev
          , fRate = rate bracket
          , fAdd = fAdd prev +
                   fRate prev * (fMax prev - fSubtract prev)
          , fMax = top bracket }

x = 3
