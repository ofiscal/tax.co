{-# LANGUAGE ScopedTypeVariables #-}

module MarginalTaxRates.Test where

import Test.HUnit
import MarginalTaxRates
import Data.Either (isLeft, isRight)


runTests :: IO Counts
runTests = runTestTT tests

tests :: Test
tests = TestList
  [ TestLabel "test_dropLastCondition" test_dropLastCondition
  , TestLabel "test_wrapConditions" test_wrapConditions
  , TestLabel "test_format" test_format
  , TestLabel "test_validateTable" test_validateTable
  , TestLabel "test_tableToMoneyBrackets" test_tableToMoneyBrackets
  , TestLabel "test_csvToTable" test_csvToTable
  ]

test_csvToTable :: Test
test_csvToTable = TestCase $ do
  let filename = "MarginalTaxRates/test_rates.csv"
  table :: Table <- csvToTable filename
  assertBool "" $ table ==
    ( ["ceiling", "rate"]
    , [ [10, 0.1]
      , [100, 0.2]
      , [1e50, 0.3] ] )

test_tableToMoneyBrackets :: Test
test_tableToMoneyBrackets = TestCase $ do
  let colnames = ["ceiling","rate"]
      invalid = [ [1,2]
                , [3,4] ]
      [a,b,c,d] = [10,0,100,0.1]
      valid = [ [ a,b ]
              , [ c,d ] ]
  assertBool "" $ isLeft $ tableToMoneyBrackets (colnames, invalid)
  assertBool "" $ tableToMoneyBrackets (colnames, valid) ==
    Right [ MoneyBracket a b
          , MoneyBracket c d ]

test_validateTable :: Test
test_validateTable = TestCase $ do
  let good :: Table = ( ["a","b"],
                        [ [ 0, 10 ]
                        , [ 1, 100 ] ] )
      bad :: Table = ( ["a","b"], [[0]] )
      exact = [(0,1), (0,100)]
      tight = [ (0.2,0.3),
                (10,20) ]
      loose = replicate 2 (-1e4,1e4)
  assertBool "1" $ isLeft  $ validateTable ["c"]     exact good
  assertBool "2" $ isLeft  $ validateTable ["a","b"] tight good
  assertBool "3" $ isLeft  $ validateTable ["a","b"] exact bad
  assertBool "4" $ isRight $ validateTable ["a","b"] exact good
  assertBool "5" $ isRight $ validateTable ["a","b"] loose good

test_format :: Test
test_format = TestCase $ do
  let mb = MoneyBracket
  assertBool "" $
    formulasToPython (bracketsToFormulas [ mb 0 0
                                       , mb 0.1 10
                                       , mb 0.2 100 ] )
    == [ "  return ( (x - 0.0 * muvt)*0.0 + 0.0*muvt if x < (0.0*muvt)"
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
