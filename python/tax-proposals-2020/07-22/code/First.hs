-- | The first proposal.
--
-- This is Haskell code that generates Python code.
-- For an example of how it is used, see the function
-- `non_dividend_income_tax` in `python/regime/r2018.py`.

{-# LANGUAGE NumericUnderscores #-}
module First where

import MarginalTaxRatesToPython


-- ** Data

-- * Dividend tax rates

-- Main> go dividendFormula1 dividendBrackets
-- 0                                if x < (300*muvt)
-- (x - 300  * muvt)*0.1            if x < (600*muvt)
-- (x - 600  * muvt)*0.12 + 30*muvt if x < (1000*muvt)
-- (x - 1000 * muvt)*0.18 + 78*muvt if x < (1500*muvt)
-- (x - 1500 * muvt)*0.2  + 168*muvt otherwise

-- | If your dividend income is less than 300 UVT,
-- you pay nothing in taxes on it.
dividendFormula1 :: Formula
dividendFormula1 = Formula 0 0 0 300

-- | Don't include the first bracket,
-- as it's already been converted into a Formula (`dividendFormula1`).
dividendBrackets :: [MoneyBracket]
dividendBrackets =
  [ MoneyBracket 600  0.1
  , MoneyBracket 1000 0.12
  , MoneyBracket 1500 0.18
  , MoneyBracket 9e20 0.2 ]


-- * Income tax rates

-- Main> go incomeFormula1 incomeBrackets
-- 0                                    if x < (1090*muvt)
-- (x - 1090  * muvt)*0.19              if x < (1700*muvt)
-- (x - 1700  * muvt)*0.28 + 116  *muvt if x < (4100*muvt)
-- (x - 4100  * muvt)*0.33 + 788  *muvt if x < (8670*muvt)
-- (x - 8670  * muvt)*0.35 + 2296 *muvt if x < (18970*muvt)
-- (x - 18970 * muvt)*0.39 + 5901 *muvt if x < (27595*muvt)
-- (x - 27595 * muvt)*0.44 + 9265 *muvt if x < (36000*muvt)
-- (x - 36000 * muvt)*0.47 + 12963*muvt if x < (55000*muvt)
-- (x - 55000 * muvt)*0.5  + 21893*muvt if x < (90000*muvt)
-- (x - 90000 * muvt)*0.55 + 39393*muvt otherwise

-- The table in the proposal differs slightly from this:
-- written like the above pseudo-Python, its last row would look like this:
-- (x - 56000 * muvt)*0.55 + 39393*muvt otherwise

-- | If your income is less than 300 UVT, you pay nothing in taxes on it.
incomeFormula1 :: Formula
incomeFormula1 = Formula 0 0 0 1090

-- | Don't include the first bracket,
-- as it's already been converted into a Formula (`incomeFormula1`).
incomeBrackets :: [MoneyBracket]
incomeBrackets =
  [ MoneyBracket  1_700 0.19
  , MoneyBracket  4_100 0.28
  , MoneyBracket  8_670 0.33
  , MoneyBracket 18_970 0.35
  , MoneyBracket 27_595 0.39
  , MoneyBracket 36e3   0.44
  , MoneyBracket 55e3   0.47
  , MoneyBracket 90e3   0.5
  , MoneyBracket 9e20   0.55 ]


-- * Corporate wealth tax rates

-- What I calculate from the proposal's thresholds and (implicit) rates:
-- 0                                   if x < 1207628
-- (x -     1207628)*0.04              if x < 2190581
-- (x -     2190581)*0.045 + 39318.117 if x < 3454377
-- (x -     3454377)*0.05  + 96188.94  if x < 1.7665066e7
-- (x - 1.7665066e7)*0.055 + 806723.4  if x < 4.2126548e7
-- (x - 4.2126548e7)*0.06  + 2152105   if x < Infinity

-- The proposal is not quite that:
-- 0                                     if x < 1207628
-- (x -        145000)*0.04              if x < 2190581
-- (x -       2190581)*0.045 + 39318.117 if x < 3454377
-- (x -       3454377)*0.05  + 96188.94  if x < 1.7665066e7
-- (x -   1.7665066e7)*0.055 + 806723.4  if x < 4.2126548e7
-- (x - 280843660)*0.06  + 2152105   if x < Infinity

-- | If your wealth is less than 300 UVT, you pay nothing in taxes on it.
corporateWealthFormula1 :: Formula
corporateWealthFormula1 = Formula 0 0 0 1_207_628

-- | Don't include the first bracket,
-- as it's already been converted into a Formula (`corporateWealthFormula1`).
corporateWealthBrackets :: [MoneyBracket]
corporateWealthBrackets =
  [ MoneyBracket  2_190_581 0.04
  , MoneyBracket  3_454_377 0.045
  , MoneyBracket 17_665_066 0.05
  , MoneyBracket 42_126_548 0.055
  , MoneyBracket 9e50       0.06 ]


-- * Inheritance tax rates

-- What I calculate from the proposal's thresholds and marginal rates:
-- Main> go inheritanceFormula1 inheritanceBrackets
-- 0                                           if x < ( 112337*muvt)
-- (x -  112337 * muvt)*0.1                    if x < ( 280884*muvt)
-- (x -  280884 * muvt)*0.2  +  16854.701*muvt if x < (2808436*muvt)
-- (x - 2808436 * muvt)*0.33 + 522365.1*muvt   if x <    (9e20*muvt)

-- Formulas contained in the proposal are different:
-- 0                                       if x < ( 112337*muvt)
-- x                   *0.1                if x < ( 280884*muvt)
-- (x -  280884 * muvt)*0.2  +  28084*muvt if x < (2808436*muvt)
-- (x - 2808436 * muvt)*0.25 + 533594*muvt if x <    (9e20*muvt)

-- | If your inheritance is less than 300 UVT, you pay nothing in taxes on it.
inheritanceFormula1 :: Formula
inheritanceFormula1 = Formula 0 0 0 112_337

-- | Don't include the first bracket,
-- as it's already been converted into a Formula (`inheritanceFormula1`).
inheritanceBrackets :: [MoneyBracket]
inheritanceBrackets =
  [ MoneyBracket    280_884 0.1
  , MoneyBracket  2_808_436 0.2
  , MoneyBracket  9e20      0.33 ]


-- * Wealth tax rates

-- What I calculate from the proposal's thresholds and (implicit) rates:
-- Main> go wealthFormula1 wealthBrackets
-- 0                                                 if x < (84253*muvt)
-- else (x -   84253 * muvt)*1e-2                    if x < (140422*muvt)
-- else (x -  140422 * muvt)*1.5e-2 + 561.69*muvt    if x < (280844*muvt)
-- else (x -  280844 * muvt)*2e-2   + 2668.0198*muvt if x < (702109*muvt)
-- else (x -  702109 * muvt)*2.5e-2 + 11093.319*muvt if x < (1404218*muvt)
-- else (x - 1404218 * muvt)*3e-2   + 28646.043*muvt if x < (2106327*muvt)
-- else (x - 2106327 * muvt)*3.5e-2 + 49709.313*muvt if x < (2808437*muvt)
-- else (x - 2808437 * muvt)*4e-2   + 74283.164*muvt

-- Formulas from the proposal are different:
-- 0                                            if x <   (84253*uvt)
-- else (x -    13500 * uvt)*1e-2               if x <  (140422*uvt)
-- else (x -   140422 * uvt)*1.5e-2 +  1269*uvt if x <  (280844*uvt)
-- else (x -   280843 * uvt)*2e-2   +  3376*uvt if x <  (702109*uvt)
-- else (x -   969796 * uvt)*2.5e-2 + 11801*uvt if x < (1404218*uvt)
-- else (x -  1685061 * uvt)*3e-2   + 29354*uvt if x < (2106327*uvt)
-- else (x -  2106327 * uvt)*3.5e-2 + 50417*uvt if x < (2808437*uvt)
-- else (x - 14042183 * uvt)*4e-2   + 74990*uvt
  -- The richest would by these rules exempt 14042183,
  -- rather than the 2808437 that I calculate.
  -- The former random-looking figure is precisely 5 times the latter.

-- | If your wealth is less than 300 UVT, you pay nothing in taxes on it.
wealthFormula1 :: Formula
wealthFormula1 = Formula 0 0 0 84253

-- | Don't include the first bracket,
-- as it's already been converted into a Formula (`wealthFormula1`).
wealthBrackets :: [MoneyBracket]
wealthBrackets =
  [ MoneyBracket   140_422 0.01
  , MoneyBracket   280_844 0.015
  , MoneyBracket   702_109 0.02
  , MoneyBracket 1_404_218 0.025
  , MoneyBracket 2_106_327 0.03
  , MoneyBracket 2_808_437 0.035
  , MoneyBracket 9e20      0.04 ]
