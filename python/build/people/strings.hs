-- This script was used to create the boilerplate in
-- python/build/names_in_tables.py

import Text.Regex


safeSubRegex :: String -> String -> String -> String
safeSubRegex pat replacement s =
  let p = mkRegex pat
  in if matchRegex p s == Nothing then s
     else subRegex p s replacement

stripQuotes :: String -> String
stripQuotes = safeSubRegex "\"" ""

toUnderscore :: String -> String
toUnderscore = safeSubRegex "[ ,:\\-]+" "_"

giveVarName :: String -> String
giveVarName s = toUnderscore s ++ " =\n  \"" ++ s ++ "\""

main :: IO ()
main =
  let doLine = giveVarName . stripQuotes
  in readFile "input.txt" >>=
     return . unlines . map doLine . lines >>=
     writeFile "output.txt"
