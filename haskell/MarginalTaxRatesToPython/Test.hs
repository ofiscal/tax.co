module MarginalTaxRatesToPython.Test where

import Test.HUnit
import MarginalTaxRatesToPython


runTests :: IO Counts
runTests = runTestTT tests

tests :: Test
tests = TestList
  [ TestLabel "test_dropLastCondition" test_dropLastCondition
  , TestLabel "test_wrapConditions" test_wrapConditions
  , TestLabel "test_format" test_format
  ]

test_format :: Test
test_format = TestCase $ do
  let mb = MoneyBracket
  assertBool "" $
    formatFormulas (bracketsToFormulas [ mb 0 0
                                       , mb 0.1 10
                                       , mb 0.2 100 ] )
    == [ "def f(x):"
       , "  return ( (x - 0.0 * muvt)*0.0 + 0.0*muvt if x < (0.0*muvt)"
       , "  else ( (x - 0.0 * muvt)*10.0 + 0.0*muvt if x < (0.1*muvt)"
       , "  else ( (x - 0.1 * muvt)*100.0 + 1.0*muvt "
       , "  )))" ]

test_wrapConditions :: Test
test_wrapConditions = TestCase $ do
  assertBool "" $ wrapConditions ["a","b"]
    == ["return ( a", "else ( b", "))" ]

test_dropLastCondition :: Test
test_dropLastCondition = TestCase $ do
  assertBool "" $ dropLastCondition ["big", "bird", "flies"]
    == ["big","bird","fl"]
