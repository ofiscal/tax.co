module MarginalTaxRatesToPython.Test where

import Test.HUnit
import MarginalTaxRatesToPython


allTests :: IO Counts
allTests = runTestTT tests

tests :: Test
tests = TestList
  [ TestLabel "test_x" test_x ]

test_x :: Test
test_x = TestCase $ do
  let scheme = ( Formula 0 0 0 
               , [ MoneyBracket    280_884 0.1
                 , MoneyBracket  2_808_436 0.2
                 , MoneyBracket  9e50      0.33 ] )
