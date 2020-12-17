-- | Usage: from the command line (in the Docker container), run
--   runhaskell haskell/args.hs a b
-- and if main = readArgs, this will print the first arg, i.e. `a`.
-- If main = readCsv, the arguments will be ignored,
-- and this will instead print the first numeric line of test.csv.

{-# LANGUAGE ScopedTypeVariables #-}

import System.Environment (getArgs)
import Data.List.Split (splitOn)


main = readCsv

readArgs = do
  s <- getArgs
  putStrLn $ head s

readCsv = do
  elts :: [[String]] <-
    tail . map (splitOn ",") . lines
    <$> readFile "haskell/test.csv"
  putStrLn $ show $ head elts
