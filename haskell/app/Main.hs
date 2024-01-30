{-# LANGUAGE ScopedTypeVariables #-}

module Main where

import System.Environment (getArgs)
import System.Exit as SE
import MarginalTaxRates (csvToPython)


main :: IO ()
main = do
  (name_without_extension:_) <- getArgs
  let inFile = name_without_extension ++ ".csv"
      outFile = name_without_extension ++ ".py"
  ess :: Either String [String] <-
    csvToPython inFile
  case ess of
    Left s -> do putStrLn s
                 SE.exitWith $ ExitFailure 1
    Right ss -> writeFile outFile $ unlines ss
