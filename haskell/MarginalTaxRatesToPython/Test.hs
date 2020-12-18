module MarginalTaxRatesToPython.Test where

import Test.HUnit
import MarginalTaxRatesToPython


runTests :: IO Counts
runTests = runTestTT tests

tests :: Test
tests = TestList
  [ TestLabel "test_x" test_x ]

test_x :: Test
test_x = TestCase $ do
  return ()
