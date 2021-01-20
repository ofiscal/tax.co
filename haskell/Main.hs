module Main where

import System.Environment (getArgs)
import MarginalTaxRates


main :: IO ()
main = getArgs >>= mapM_ putStrLn
