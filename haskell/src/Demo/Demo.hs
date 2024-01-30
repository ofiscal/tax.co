-- | If main = readArgs, this will print the first arg, i.e. `a`.
-- If main = readCsv, the arguments will be ignored,
-- and this will print the first numeric line of test.csv.
-- If main = proveImport, the arguments will be ignored,
-- and this will print the value of `Share.Test.x`.

{-# LANGUAGE ScopedTypeVariables #-}

module Demo.Demo where

import System.Environment (getArgs)
import Data.List.Split (splitOn)
import Demo.Share.Test (x)


main = proveImport

proveImport = putStrLn $ show x

readArgs = do
  s <- getArgs
  putStrLn $ head s

readCsv = do
  elts :: [[String]] <-
    tail . map (splitOn ",") . lines
    <$> readFile "test.csv"
  putStrLn $ show $ head elts
