module MarginalTaxRatesToPython.Test where

import Test.HUnit
import MarginalTaxRatesToPython


runTests :: IO Counts
runTests = runTestTT tests

tests :: Test
tests = TestList
  [ TestLabel "test_dropLastCondition" test_dropLastCondition ]

test_dropLastCondition :: Test
test_dropLastCondition = TestCase $ do
  assertBool "" $ dropLastCondition ["big", "bird", "flies"]
    == ["big","bird","fl"]
