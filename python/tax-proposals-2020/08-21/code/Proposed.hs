-- | This is Haskell code that generates Python code.
-- For an example of how it is used, see the function
-- `non_dividend_income_tax` in `python/regime/r2018.py`.

{-# LANGUAGE NumericUnderscores #-}
module First where

import MarginalTaxRatesToPython


data Tax
   = Dividend
   -- No "WealthCorporate" because those rates depend on size, not income.
   | IncomePerson
   | Inheritance
   | WealthCorporate
   | WealthPerson

go' :: Tax -> IO ()
go' tax = let (initFormula, brackets) = scheme tax
          in go initFormula brackets

scheme :: Tax -> (Formula, [MoneyBracket])

scheme Dividend =
  ( Formula 0 0 0 300
  , [ MoneyBracket 600  0.1
    , MoneyBracket 1000 0.12
    , MoneyBracket 1500 0.18
    , MoneyBracket 9e50 0.2 ] )

scheme IncomePerson =
  ( Formula 0 0 0 1090
  , [ MoneyBracket  1_700 0.19
    , MoneyBracket  4_100 0.28
    , MoneyBracket  8_670 0.33
    , MoneyBracket 18_970 0.35
    , MoneyBracket 27_595 0.39
    , MoneyBracket 36e3   0.44
    , MoneyBracket 55e3   0.47
    , MoneyBracket 90e3   0.5
    , MoneyBracket 9e50   0.55 ] )

scheme Inheritance =
  ( Formula 0 0 0     112_337
  , [ MoneyBracket    280_884 0.1
    , MoneyBracket  2_808_436 0.2
    , MoneyBracket  9e50      0.33 ] )

scheme WealthCorporate =
  ( Formula 0 0 0   1_207_628
  , [ MoneyBracket  2_190_581 0.04
    , MoneyBracket  3_454_377 0.045
    , MoneyBracket 17_665_066 0.05
    , MoneyBracket 42_126_548 0.055
    , MoneyBracket 9e50       0.06 ] )

scheme WealthPerson =
  ( Formula 0 0 0 84253
  , [ MoneyBracket   140_422 0.01
    , MoneyBracket   280_844 0.015
    , MoneyBracket   702_109 0.02 
    , MoneyBracket 1_404_218 0.025
    , MoneyBracket 2_106_327 0.03
    , MoneyBracket 2_808_437 0.035
    , MoneyBracket 9e50      0.04 ] )
