-- This is Haskell, not Python.
-- Developing the income tax code was easier in this language.

data IncomeBracket = IncomeBracket
  { top :: Float
  , rate :: Float } deriving (Show)

data Formula = Formula
  { fSubtract :: Float
  , fRate :: Float
  , fAdd :: Float
  , fMax :: Float }

instance Show Formula where
  show f = "(x - " ++ show (fSubtract f) ++ " * muvt)*" ++
           show (fRate f) ++ " + " ++ show (fAdd f)
           ++ "*muvt if x < (" ++ show (fMax f) ++ "*muvt)"

-- | If you make less than 1090, you pay nothing in taxes.
regime2018 :: [IncomeBracket]
regime2018 =
  [ IncomeBracket 1700       0.19
  , IncomeBracket 4100       0.28
  , IncomeBracket 8670       0.33
  , IncomeBracket 18970      0.35
  , IncomeBracket 31000      0.37
  , IncomeBracket 9999999999 0.39 ]

f :: Formula -> IncomeBracket -> Formula
f prev bracket =
  Formula { fSubtract = fMax prev
          , fRate = rate bracket
          , fAdd = fAdd prev +
                   fRate prev * (fMax prev - fSubtract prev)
          , fMax = top bracket }

formulae :: [Formula]
formulae = scanl f (Formula 0 0 0 1090) regime2018

main :: IO ()
main = mapM_ (putStrLn . show) formulae
